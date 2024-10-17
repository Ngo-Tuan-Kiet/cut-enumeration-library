def discharge(u):
    """
    Discharges the excess flow from node u.
    """
    while G.nodes[u]['excess'] > 0:
        pushed = False  # Flag to track if any push happens
        for v in G.neighbors(u):
            # Check forward push conditions: capacity and height
            if G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0 and G.nodes[u]['height'] == G.nodes[v]['height'] + 1:
                push(u, v)
                pushed = True  # We successfully pushed some flow forward
                if G.nodes[u]['excess'] == 0:  # No more excess, stop discharge
                    break

        if not pushed:  # If we couldn't push forward, try relabel or consider backflow
            relabel(u)  # Attempt to relabel first to try pushing forward again
            
            # Now check backflow if all forward pushes are impossible and relabel didn't help
            if G.nodes[u]['excess'] > 0:
                for v in G.neighbors(u):
                    # Check if we can push back to u (reverse flow on edge v -> u)
                    if G.edges[v, u]['preflow'] < 0:  # Only if there's negative flow, i.e., flow from u to v
                        send_back = min(G.nodes[u]['excess'], -G.edges[v, u]['preflow'])
                        G.nodes[u]['excess'] -= send_back
                        G.nodes[v]['excess'] += send_back
                        G.edges[v, u]['preflow'] += send_back  # Reduce negative preflow
                        G.edges[u, v]['preflow'] -= send_back  # Adjust preflow in opposite direction
                        
                        # If v gets excess after backflow, mark it as active
                        if G.nodes[v]['excess'] > 0 and v not in ACTIVE_NODES:
                            ACTIVE_NODES.append(v)
                        
                        if G.nodes[u]['excess'] == 0:  # No more excess, stop discharge
                            break

    # Ensure u is still an active node if it has excess after discharge
    if G.nodes[u]['excess'] > 0 and u not in ACTIVE_NODES:
        ACTIVE_NODES.append(u)