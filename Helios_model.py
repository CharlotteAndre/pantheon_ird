from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

matplotlib.use('TkAgg')
from pythonis_model import *
import networkx as nx



def createListPanelGraph(flow):
    list_panel = []
    for i in range(len(flow)):
        list_panel.append(i)
    return list_panel


def drawGraph(genes_names_list, network_as_list, flow, graph_selected, layout_selected, color_activate_node,
              color_inactivate_node, color_active_edge, color_inactivate_edge, activate_widthedge,genes_selected_visu):

    G = nx.MultiDiGraph()
    value_source = getFlow(flow, graph_selected)
    global_gene_state = getRegulationActivation(network_as_list, genes_names_list, value_source)
    # ajout des aretes et des noeuds
    G = addNodes(global_gene_state, G)
    G = addEdges(network_as_list, G)
    G = drawFig(G, global_gene_state, layout_selected, color_activate_node, color_inactivate_node,
                     color_active_edge, color_inactivate_edge, activate_widthedge, genes_selected_visu)

    return G


def drawFig(G, global_gene_state, layout_selected, color_activate_node, color_inactivate_node, color_active_edge,
            color_inactivate_edge, activate_widthedge, genes_selected_visu):
    pos = selectLayout(G, layout_selected)
    for node in G.nodes(data=True):
        transparency = 1
        if node[1]['forme'] == "1":
            node_shape = "^"
        if node[1]['forme'] == "-1":
            node_shape = "v"
        if node[1]['forme'] == "0":
            node_shape = "o"
        if node[1]['active_state'] == 0:
            color = color_inactivate_node
        if node[1]['active_state'] == 1:
            color = color_activate_node
        if genes_selected_visu :
            transparency = 0.5
            for i in range(len(genes_selected_visu)):
                if genes_selected_visu[i] == node[0]:
                    transparency = 1
        nx.draw_networkx_nodes(G, pos, nodelist=[node[0]], node_size=1500, node_shape= node_shape, node_color= color, alpha = transparency)

    nx.draw_networkx_labels(G, pos)
    for edge in G.edges(data=True):
        if edge[2]['arrowstyle'] == "-1":
            arrowstyle = "-["
        if edge[2]['arrowstyle'] == "1":
            arrowstyle = "-|>"
        if edge[2]['duet'] == "1":
            form_arrow = 'arc3, rad = 0.2'
        if edge[2]['duet'] == "0":
            form_arrow = 'arc3, rad = 0.0'
        for i in range(len(global_gene_state)):
            if global_gene_state[i][0] == edge[0]:
                if global_gene_state[i][1] == 1:
                    activateedge = color_active_edge
                    widthedge = activate_widthedge
                else:
                    activateedge = color_inactivate_edge
                    widthedge = 1

        nx.draw_networkx_edges(G, pos, edgelist=[(edge[0], edge[1])], width=widthedge, arrowstyle=arrowstyle,
                               node_size=1900, connectionstyle=form_arrow, edge_color=activateedge)

    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0.25,
                        wspace=0.35)
    plt.ioff()
    plt.draw()
    fig = plt.gcf()
    return fig,G


def getFlow(flow, graph_selected):
    value_to_reach = graph_selected + 1
    value_running = 0
    for key, value in flow.items():
        # Cle du dictionnaire
        value_source = []
        source = key
        value_running += 1
        if value_running == value_to_reach:
            for number in source:
                value_source.append(number)
            return value_source

def getRegulationActivation(network_as_list, genes_names_list, value_source):
    positive_gene = []
    negative_gene = []
    global_gene_state = []

    for i in range(len(network_as_list)):
        gene_source = network_as_list[i][0]
        gene_target = network_as_list[i][2]
        interaction = network_as_list[i][1]
        if gene_target == gene_source:
            if interaction == "1":
                positive_gene.append(gene_source)

            else:
                negative_gene.append(gene_source)

    for i in range(len(genes_names_list)):
        state_gene = []
        gene = genes_names_list[i]
        activation = value_source[i]
        if gene in positive_gene:
            regulation = "1"
        if gene in negative_gene:
            regulation = "-1"
        else:
            regulation = "0"
        state_gene.append(gene)
        state_gene.append(activation)
        state_gene.append(regulation)
        global_gene_state.append(state_gene)
    return global_gene_state


def addEdges(network_as_list, G):
    for i in range(len(network_as_list)):
        duet = "0"
        gene_source = network_as_list[i][0]
        gene_target = network_as_list[i][2]
        interaction = network_as_list[i][1]
        for k in range(len(network_as_list)):
            if network_as_list[k][0] == gene_target and network_as_list[k][2] == gene_source:
                duet = "1"
        G.add_edge(gene_source, gene_target, arrowstyle=interaction, duet=duet)

    return G


def addNodes(global_gene_state, G):
    for i in range(len(global_gene_state)):
        gene_name = global_gene_state[i][0]
        activation = global_gene_state[i][1]
        regulation = global_gene_state[i][2]
        G.add_node(gene_name, forme=regulation, active_state=activation)
    return G


def selectLayout(G, layout_selected):
    if layout_selected == 'circular_layout':
        pos = nx.circular_layout(G)
    if layout_selected == 'spring_layout':
        pos = nx.spring_layout(G)
    if layout_selected == 'kamada_kawai_layout':
        pos = nx.kamada_kawai_layout(G)
    if layout_selected == 'random_layout':
        pos = nx.random_layout(G)
    if layout_selected == 'shell_layout':
        pos = nx.shell_layout(G)
    if layout_selected == 'spectral_layout':
        pos = nx.spectral_layout(G)
    if layout_selected == 'planar_layout':
        pos = nx.planar_layout(G)
    if layout_selected == 'fruchterman_reingold_layout':
        pos = nx.fruchterman_reingold_layout(G)
    if layout_selected == 'spiral_layout':
        pos = nx.spiral_layout(G)
    return pos


# ------------------------------- Beginning of Matplotlib  -----------------------
######Ca c'est bon#########

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')
