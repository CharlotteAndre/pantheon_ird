import PySimpleGUI as sg
from PIL import Image
import cv2 as cv
import io
from pythonis_filesIO import *
from random_network import *
from Helios_model import *
from Helios_Refactor_Pythonis import *
from Helios_IO import *
from Helios_addElement import *
from Helios_geneGraph import *
from Helios_displayView import *
from Helios_savePNG import *
from Helios_movie import *
from Helios_checkError import *


def layoutStart():
    layout_start = [[sg.Frame(layout=[[sg.Text('Gene List File', background_color='#343434', text_color='#e4e4e4')],
                                      [sg.Input(), sg.FileBrowse()],
                                      [sg.Text('Network Structure File', background_color='#343434',
                                               text_color='#e4e4e4')],
                                      [sg.Input(), sg.FileBrowse()]],
                              title='Import network', title_color='#e4e4e4', relief=sg.RELIEF_SUNKEN,
                              background_color='#343434',
                              tooltip='Choose gene list file and network structure file to import a predefined network model')],
                    [sg.Frame(layout=[[sg.Text('Number of nodes', background_color='#343434', text_color='#e4e4e4')],
                                      [sg.Input()],
                                      [sg.Text('Number of interactions', background_color='#343434',
                                               text_color='#e4e4e4')],
                                      [sg.Input()]],
                              title='Gene network Automated Initiation Algorithm (GAIA)', title_color='#e4e4e4',
                              relief=sg.RELIEF_SUNKEN,
                              background_color='#343434',
                              tooltip='Create a random network to work with')],
                    [sg.Frame(layout=[[sg.Radio('Batch Computation Mode', 'RADIO1', default=True, size=(18, 1),
                                                background_color='#343434', text_color='#e4e4e4'),
                                       sg.Radio('Visual Network Mode', 'RADIO1', background_color='#343434',
                                                text_color='#e4e4e4')]],
                              title='Run mode', title_color='#e4e4e4', relief=sg.RELIEF_SUNKEN,
                              background_color='#343434',
                              tooltip='Batch computation for whole network simulation and genes significance study / Interactive network to quick test hypothesis manually and visually')],
                    [sg.CloseButton('Import'), sg.CloseButton('Cancel')]]
    window_start = sg.Window("Initialize Network", alpha_channel=0.95, layout=layout_start)
    return window_start


def layoutBooleanModelVisu():
    col_visu1 = [[sg.Text('Input : List of genes', text_color='#e4e4e4', background_color='#343434')],
                 [sg.Listbox(values=genes_names_list,
                             select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(20, 35),
                             tooltip='Highlighted genes will be set to 1 at the start of each simulation run if the choice of genes initial states parameter is << specified >>')],
                 ]

    col_visu2 = [[sg.Text('Input : Interactions in the network', text_color='#e4e4e4', background_color='#343434')],
                 [sg.Listbox(values=network_as_list,
                             select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, 35),
                             tooltip='Format is [Source gene, interaction (-1: repression, 1 : activation), target gene]')],
                 ]

    # col_subbatch3 = [[sg.Listbox(values=model_type_list, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(15, 4),
    #                              tooltip='Highlight the models to run through ARGOS'),
    #                   sg.Listbox(values=boundary_model_list, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(15, 4),
    #                              tooltip='Highlight the models to run through ARGOS')]]

    col_visu3 = [[sg.Frame(layout=[[sg.Text('Model type', text_color='#e4e4e4', background_color='#343434',
                                            tooltip='Choice of rules to apply to the network structure'),
                                    sg.Combo(values=model_type_list, default_value=model_type_list[0])],
                                   [sg.Text('Boundary conditions', text_color='#e4e4e4', background_color='#343434',
                                            tooltip='Choice of behavior for nodes without regulators'),
                                    sg.Combo(values=boundary_model_list, default_value=boundary_model_list[0])],
                                   [sg.Text('Genes initial states', text_color='#e4e4e4',
                                            background_color='#343434',
                                            tooltip='In <<specified>> mode, use the gene list panel to highlight the genes to be set to 1 at start,\n all other genes will be set to 0 (0 or 1 in <<random-specified>> mode)'),
                                    sg.Combo(values=initial_states_choice_list,
                                             default_value=initial_states_choice_list[0])],
                                   [sg.Text('Number of initial states :', text_color='#e4e4e4',
                                            background_color='#343434',
                                            tooltip='Choice of how many initial states the model will run from'),
                                    sg.Radio('All possible states', 'RADIO2', background_color='#343434',
                                             text_color='#e4e4e4'),
                                    sg.Radio('Given number of states', 'RADIO2', background_color='#343434',
                                             text_color='#e4e4e4', default=True),
                                    sg.InputText(size=(10, 1), default_text='1')],
                                   [sg.Text('KO mutation type', text_color='#e4e4e4', background_color='#343434',
                                            tooltip='Choice of Knocked Out mutation to apply to the network \n- single KO will run the model mutating each chosen genes one at a time'
                                                    '\n- multiple KO will run the model once with all chosen genes as KO'
                                                    '\n- combination KO will go through all combinations of double KO for the chosen genes and run the model for each'),
                                    sg.Combo(values=KO_mutation_type_list, default_value=KO_mutation_type_list[0])],
                                   [sg.Text('List of KO genes', text_color='#e4e4e4', background_color='#343434',
                                            tooltip='Enter gene names separated by a colon e.g. ABC, LMN, XYZ'),
                                    sg.InputText()],
                                   [sg.Text('OA mutation type', text_color='#e4e4e4', background_color='#343434',
                                            tooltip='Choice of Over Activated mutation to apply to the network \n- single OA will run the model mutating each chosen genes one at a time'
                                                    '\n- multiple OA will run the model once with all chosen genes as KO'
                                                    '\n- combination OA will go through all combinations of double KO for the chosen genes and run the model for each'),
                                    sg.Combo(values=OA_mutation_type_list, default_value=OA_mutation_type_list[0])],
                                   [sg.Text('List of OA genes', text_color='#e4e4e4', background_color='#343434',
                                            tooltip='Enter gene names separated by a colon e.g. ABC, LMN, XYZ'),
                                    sg.InputText()],
                                   [sg.Button('Run HELIOS'), sg.Button('Run HELIOS 2')]
                                   ],
                           title='Predict System Fates', title_color='#e4e4e4', background_color='#343434',
                           relief=sg.RELIEF_GROOVE)],
                 [sg.Frame(layout=[
                     [sg.Text('Source', text_color='#e4e4e4', background_color='#343434',
                              tooltip='Value must a number'), sg.InputText(size=(10, 1)),
                      sg.Text('Interaction', text_color='#e4e4e4', background_color='#343434',
                              tooltip='1 for activation or -1 for inhibition'), sg.InputText(size=(10, 1)),
                      sg.Text('Target', text_color='#e4e4e4', background_color='#343434',
                              tooltip='Value must a '), sg.InputText(size=(10, 1)), sg.Button('Add element')]],
                     title='Add element to graph', title_color='#e4e4e4',
                     background_color='#343434', relief=sg.RELIEF_GROOVE)],
                 [sg.Frame(layout=[
                     [sg.Button('Add element from CSV'), sg.Input(), sg.FileBrowse()]],
                     title='Add element from CSV', title_color='#e4e4e4',
                     background_color='#343434', relief=sg.RELIEF_GROOVE)],
                 [sg.Frame(layout=[
                     [sg.Input(), sg.FileBrowse(), sg.Button("Load")]],
                     title='Load saved graph', title_color='#e4e4e4',
                     background_color='#343434', relief=sg.RELIEF_GROOVE)],
                 [sg.Text('', background_color='#343434')]]

    layout_visu = [
        [sg.Column(col_visu1, background_color='#343434'), sg.Column(col_visu2, background_color='#343434'),
         sg.Column(col_visu3, background_color='#343434')],
        [sg.Exit()]]

    window_visu = sg.Window("Initialize Network", alpha_channel=0.95, layout=layout_visu)
    return window_visu


def layoutVisuGraph(list_panel, layout_graph_drawing, layout_color_drawing, title):
    col_graphs1 = [[sg.Text('Input : List of genes', text_color='#e4e4e4', background_color='#343434')],
                   [sg.Listbox(values=genes_names_list,
                               select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(20, 15),
                               tooltip='Highlighted genes will be set to 1 at the start of each simulation run if the choice of genes initial states parameter is << specified >>')],
                   ]

    col_graphs2 = [
        [sg.Frame(layout=[
            [sg.Text('State', text_color='#e4e4e4', background_color='#343434',
                     tooltip='Select number state'),
             sg.Combo(values=list_panel, default_value=list_panel[0]),
             sg.Text('Layout', text_color='#e4e4e4', background_color='#343434'),
             sg.Combo(values=layout_graph_drawing, default_value=layout_graph_drawing[0])],
            [sg.Text('Active genes color', text_color='#e4e4e4', background_color='#343434',
                     tooltip='Select color of inactive genes'),
             sg.Combo(values=layout_color_drawing, default_value=layout_color_drawing[3]),
             sg.Text('Inactive genes color', text_color='#e4e4e4', background_color='#343434',
                     tooltip='Select color of inactive genes'),
             sg.Combo(values=layout_color_drawing, default_value=layout_color_drawing[0])],
            [sg.Text('Active interaction color', text_color='#e4e4e4', background_color='#343434',
                     tooltip='Select color of active interaction'),
             sg.Combo(values=layout_color_drawing, default_value=layout_color_drawing[10]),
             sg.Text('Inactive interaction color', text_color='#e4e4e4', background_color='#343434',
                     tooltip='Select color of inactive interaction'),
             sg.Combo(values=layout_color_drawing, default_value=layout_color_drawing[10])],
            [sg.Text('Width active Interaction', text_color='#e4e4e4', background_color='#343434',
                     tooltip='Value must a number'),
             sg.InputText(size=(5, 1), default_text="1")],
            [sg.Button('Launch visualization'),sg.Button('Display dynamic view')]],
            title='Vsualization settings', title_color='#e4e4e4',
            background_color='#343434', relief=sg.RELIEF_GROOVE)],

        [sg.Frame(layout=[
            [sg.Button('Save graph'), sg.InputText(size = (35,1))]],
            title='Save Data', title_color='#e4e4e4',
            background_color='#343434', relief=sg.RELIEF_GROOVE,tooltip='The file extension CSV will be automatically added')],
        [sg.Frame(layout=[
            [sg.Button('Save gene activity'), sg.Button("Save as video"), sg.InputText(size = (35,1))]],
            title='Save gene activity graph', title_color='#e4e4e4',
            background_color='#343434', relief=sg.RELIEF_GROOVE,
            tooltip='Save as mp4')],
        [sg.Text('', background_color='#343434')]]

    layout_graphs = [
        [sg.Column(col_graphs1, background_color='#343434'),
         sg.Column(col_graphs2, background_color='#343434')],
        [sg.Exit()]]

    window_graphs = sg.Window(title, alpha_channel=0.95, layout=layout_graphs)
    return window_graphs



folder = "F:\paperPYTHONIS\LRPnetwork-201903"
gene_list_filename = "l_gnp-221018-161genes-Ju+PI-prior.txt"
network_filename = "TDCor6.32_output_221018_parallel.txt"
KO_genes_input = ['PLT1', 'ARF6', 'LRP1', 'PHB', 'TMO5', 'SHR', 'SCR', 'SHP1', 'ATML1', 'PID2']
OA_genes_input = ['PLT7', 'PUCHI', 'CRF1', 'ARF2', 'PLT5', 'ARF9', 'ARF17', 'U.box', 'ARF19', 'WRKY43']
more_KO_genes_input = [['PLT1'], ['PLT2'], ['PLT3'], ['PLT5'], ['PLT7'], ['ARF6'], ['ARF8'], ['PLT1', 'PLT2'],
                       ['PLT5', 'PLT7'], ['ARF6', 'ARF8'], ['PLT1', 'PLT2', 'PLT3'], ['PLT3', 'PLT5', 'PLT7']]
KO_mutation_type_list = ['none', 'single KO', 'multiple KO', 'combination KO']
OA_mutation_type_list = ['none', 'single OA', 'multiple OA', 'combination OA']
model_type_list = ['logical', 'algebraic']
boundary_model_list = ['transient', 'constant']
initial_states_choice_list = ['random', 'all_zeros', 'all_ones', 'specified', 'random-specified']

if __name__ == "__main__":

    #############
    # GUI setup
    #############

    # set background globally to dark grey and text to light grey
    sg.SetOptions(text_color="#e4e4e4", font='trajanpro 11', background_color="#343434")

    # layout for the title window - as it does nothing by itself, it has to be set to autoclose after 4sec when invoked
    layout_title = [[sg.Image(r'pantheon_front_50percent.gif')], ]
    window_title = sg.Window("title", layout=layout_title, auto_close=True, auto_close_duration=4, no_titlebar=True)
    event_title, values_title = window_title.Read()
    window_title.Close()

    while True :
        window_start = layoutStart()
        event_start, values_start = window_start.Read()
        window_start.Close()

        genes_list_filename = values_start[0]
        network_filename = values_start[1]
        GAIA_genes = values_start[2]
        GAIA_interactions = values_start[3]
        launchBatch = values_start[4]
        launchVisu = values_start[5]

        check_init_gene_list, error_path = checkPath(genes_list_filename)
        check_init_interaction, error_path = checkPath(network_filename)
        if check_init_interaction == False :
            sg.popup_error("Interaction file doesn't exist in specified folder")
        if check_init_gene_list == False :
            sg.popup_error("Genes list file doesn't exist in specified folder")


        if check_init_gene_list == True  and check_init_interaction == True :
            check_format_gene_list = checkFormatGeneList(genes_list_filename)
            check_format_interaction = checkFormatInteraction(network_filename)
            if check_format_interaction == False :
                sg.popup_error("Interaction file format is wrong")
            if check_format_gene_list == False :
                sg.popup_error("Gene file format is wrong")

            if check_format_gene_list == True and check_format_interaction == True :
        #########mettre condition If pour l'ouverture du batch mode ou de la visualisation
                if launchBatch:
                    if (GAIA_genes != '') and (GAIA_interactions != ''):
                        RandomGRN1("F:/paperPYTHONIS/LRPNetwork-201903/files_to_run".decode("utf-8"),
                                   genes_list_file='GAIA_genes.txt',
                                   network_structure_file='GAIA_network.txt', number_of_nodes=GAIA_genes,
                                   number_of_edges=GAIA_interactions)
                        genes_names_list, network_dictionary, unused_genes, network_as_list, genes_non_sort = ImportBooleanModel(
                            "F:/paperPYTHONIS/LRPNetwork-201903/files_to_run/GAIA_genes.txt",
                            "F:/paperPYTHONIS/LRPNetwork-201903/files_to_run/GAIA_network.txt")
                    else:
                        genes_names_list, network_dictionary, unused_genes, network_as_list, genes_non_sort = ImportBooleanModel(
                            genes_list_filename,
                            network_filename)

                    # Columns layout for the batch mode window
                    col_batch1 = [[sg.Text('Input : List of genes', text_color='#e4e4e4', background_color='#343434')],
                                  [sg.Listbox(values=genes_names_list,
                                              select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(20, 35),
                                              tooltip='Highlighted genes will be set to 1 at the start of each simulation run if the choice of genes initial states parameter is << specified >>')],
                                  ]

                    col_batch2 = [
                        [sg.Text('Input : Interactions in the network', text_color='#e4e4e4', background_color='#343434')],
                        [sg.Listbox(values=network_as_list,
                                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, 35),
                                    tooltip='Format is [Source gene, interaction (-1: repression, 1 : activation), target gene]')],
                    ]

                    col_subbatch3 = [[sg.Listbox(values=model_type_list, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(15, 4),
                                                 tooltip='Highlight the models to run through ARGOS'),
                                      sg.Listbox(values=boundary_model_list, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                                                 size=(15, 4),
                                                 tooltip='Highlight the models to run through ARGOS')]]

                    col_batch3 = [[sg.Frame(layout=[[sg.Text('Model type', text_color='#e4e4e4', background_color='#343434',
                                                             tooltip='Choice of rules to apply to the network structure'),
                                                     sg.Combo(model_type_list)],
                                                    [sg.Text('Boundary conditions', text_color='#e4e4e4',
                                                             background_color='#343434',
                                                             tooltip='Choice of behavior for nodes without regulators'),
                                                     sg.Combo(boundary_model_list)],
                                                    [sg.Text('Genes initial states', text_color='#e4e4e4',
                                                             background_color='#343434',
                                                             tooltip='In <<specified>> mode, use the gene list panel to highlight the genes to be set to 1 at start,\n all other genes will be set to 0 (0 or 1 in <<random-specified>> mode)'),
                                                     sg.Combo(initial_states_choice_list)],
                                                    [sg.Text('Number of initial states :', text_color='#e4e4e4',
                                                             background_color='#343434',
                                                             tooltip='Choice of how many initial states the model will run from'),
                                                     sg.Radio('All possible states', 'RADIO2', background_color='#343434',
                                                              text_color='#e4e4e4'),
                                                     sg.Radio('Given number of states', 'RADIO2', background_color='#343434',
                                                              text_color='#e4e4e4', default=True),
                                                     sg.InputText(size=(10, 1), default_text='1')],
                                                    [sg.Text('KO mutation type', text_color='#e4e4e4', background_color='#343434',
                                                             tooltip='Choice of Knocked Out mutation to apply to the network \n- single KO will run the model mutating each chosen genes one at a time'
                                                                     '\n- multiple KO will run the model once with all chosen genes as KO'
                                                                     '\n- combination KO will go through all combinations of double KO for the chosen genes and run the model for each'),
                                                     sg.Combo(KO_mutation_type_list)],
                                                    [sg.Text('List of KO genes', text_color='#e4e4e4', background_color='#343434',
                                                             tooltip='Enter gene names separated by a colon e.g. ABC, LMN, XYZ'),
                                                     sg.InputText()],
                                                    [sg.Text('OA mutation type', text_color='#e4e4e4', background_color='#343434',
                                                             tooltip='Choice of Over Activated mutation to apply to the network \n- single OA will run the model mutating each chosen genes one at a time'
                                                                     '\n- multiple OA will run the model once with all chosen genes as KO'
                                                                     '\n- combination OA will go through all combinations of double KO for the chosen genes and run the model for each'),
                                                     sg.Combo(OA_mutation_type_list)],
                                                    [sg.Text('List of OA genes', text_color='#e4e4e4', background_color='#343434',
                                                             tooltip='Enter gene names separated by a colon e.g. ABC, LMN, XYZ'),
                                                     sg.InputText()],
                                                    [sg.Button('Run PYTHONIS')]
                                                    ],
                                            title='Predict System Fates', title_color='#e4e4e4', background_color='#343434',
                                            relief=sg.RELIEF_GROOVE)],
                                  [sg.Text('', background_color='#343434')],
                                  [sg.Frame(
                                      layout=[[sg.Text('Number of iterations', text_color='#e4e4e4', background_color='#343434',
                                                       tooltip='Size of the sample of random states that will be used as starting points for ARGOS'),
                                               sg.InputText(size=(8, 1), default_text='1')],
                                              [sg.Text('Choose the models to run through ARGOS :', text_color='#e4e4e4',
                                                       background_color='#343434')],
                                              [sg.Column(col_subbatch3, background_color='#343434')],
                                              [sg.Button('Run ARGOS')]],
                                      title='Automatically Research Genes Of Significance', title_color='#e4e4e4',
                                      background_color='#343434', relief=sg.RELIEF_GROOVE)],
                                  [sg.Text('', background_color='#343434')],
                                  [sg.Frame(
                                      layout=[[sg.Text('Placeholder - WIP algo', text_color='#e4e4e4', background_color='#343434',
                                                       tooltip='This will house the APOLLO algo call')],
                                              [sg.Text('Current Fate :', text_color='#e4e4e4', background_color='#343434'),
                                               sg.InputText()],
                                              [sg.Text('Targeted Fate :', text_color='#e4e4e4', background_color='#343434'),
                                               sg.InputText()],
                                              [sg.Button('Run APOLLO')]],
                                      title='Challenge Fates', title_color='#e4e4e4', background_color='#343434',
                                      relief=sg.RELIEF_GROOVE)]
                                  ]

                    layout_batchmode = [
                        [sg.Column(col_batch1, background_color='#343434'), sg.Column(col_batch2, background_color='#343434'),
                         sg.Column(col_batch3, background_color='#343434')],
                        [sg.Text('Extract core network :', text_color='#e4e4e4', background_color='#343434'),
                         sg.Button('Run HEPHAISTOS')],
                        [sg.Button('Back to files import'), sg.Exit()]]

                    window_batch = sg.Window("Batch Mode", alpha_channel=0.95, layout=layout_batchmode)

                    # output window layout
                    layout_pythonis_output = [[sg.Output(size=(80, 20))],
                                              [sg.Button('Update prediction', button_color=(sg.YELLOWS[0], sg.BLUES[0]))]
                                              ]

                    window_pythonis_output = sg.Window('Pythonis Prediction', alpha_channel=0.95, layout=layout_pythonis_output,
                                                       default_element_size=(30, 2))

                    # TODO update this call to read the working directory from GUI file import
                    # os.chdir("LRPNetwork-201903/files_to_run/output")

                    while True:
                        event_batch, values_batch = window_batch.Read()

                        # catch all parameters from the GUI
                        genes_selected = values_batch[0]
                        interactions_selected = values_batch[1]
                        boolean_model_selected = values_batch[2]
                        boundary_model_selected = values_batch[3]
                        initial_state_selected = values_batch[4]
                        all_initial_states_bool = values_batch[5]
                        subset_initial_states_bool = values_batch[6]
                        number_initial_states = values_batch[7]
                        KO_type_selected = values_batch[8]
                        if KO_type_selected != 'none':
                            KO_genes_selected = values_batch[9]
                            KO_genes_selected = KO_genes_selected.rsplit(',')
                        else:
                            KO_genes_selected = ['foo']
                        OA_type_selected = values_batch[10]
                        if OA_type_selected != 'none':
                            OA_genes_selected = values_batch[11]
                            OA_genes_selected = OA_genes_selected.rsplit(',')
                        else:
                            OA_genes_selected = ['foo']
                        number_iteration_ARGOS = values_batch[12]
                        boolean_model_ARGOS = values_batch[13]
                        boundary_model_ARGOS = values_batch[14]
                        current_fate = values_batch[15]
                        target_fate = values_batch[16]

                        # launch modules or exit depending on button pushed
                        if event_batch is None or event_batch == 'Exit':
                            break
                        elif event_batch == 'Run PYTHONIS':
                            if all_initial_states_bool:
                                flow, stable, start, stable_states, initial_states, genes_names, data, network, time = RunBooleanModel(
                                    genes_names=genes_names_list, genes_network=network_dictionary, initial_state_number='all',
                                    initial_state_choice=initial_state_selected,
                                    model=boolean_model_selected, stimulus=boundary_model_selected,
                                    initial_state_genes=genes_selected,
                                    KO_genes=KO_genes_selected, OA_genes=OA_genes_selected)

                                resMod(genes_names_list, network_dictionary, start, flow, stable, genes_list_filename,
                                       network_filename,
                                       genes_names, KO_genes_selected, OA_genes_selected, boolean_model_selected,
                                       boundary_model_selected, network, initial_states, stable_states, data)

                            elif subset_initial_states_bool:
                                event, value = window_pythonis_output.Read()
                                flow, stable, start, stable_states, initial_states, genes_names, data, network, time = RunBooleanModel(
                                    genes_names=genes_names_list, genes_network=network_dictionary,
                                    initial_state_number=number_initial_states, initial_state_choice=initial_state_selected,
                                    model=boolean_model_selected, stimulus=boundary_model_selected,
                                    initial_state_genes=genes_selected,
                                    KO_genes=KO_genes_selected, OA_genes=OA_genes_selected)

                                resMod(genes_names_list, network_dictionary, start, flow, stable, genes_list_filename,
                                       network_filename,
                                       genes_names, KO_genes_selected, OA_genes_selected, boolean_model_selected,
                                       boundary_model_selected, network, initial_states, stable_states, data)

                            else:
                                sg.Popup(
                                    'Please select value for number of initial states ( <<all>> or enter numerical value ) and run PYTHONIS again',
                                    no_titlebar=True, background_color='#343434')

                    window_batch.Close()

                ###################Visualization#######################

                if launchVisu:
                    if (GAIA_genes != '') and (GAIA_interactions != ''):
                        RandomGRN1("F:/paperPYTHONIS/LRPNetwork-201903/files_to_run".decode("utf-8"),
                                   genes_list_file='GAIA_genes.txt',
                                   network_structure_file='GAIA_network.txt', number_of_nodes=GAIA_genes,
                                   number_of_edges=GAIA_interactions)
                        genes_names_list, network_dictionary, unused_genes, network_as_list, genes_non_sort = ImportBooleanModel(
                            "F:/paperPYTHONIS/LRPNetwork-201903/files_to_run/GAIA_genes.txt",
                            "F:/paperPYTHONIS/LRPNetwork-201903/files_to_run/GAIA_network.txt")
                    else:
                        genes_names_list, network_dictionary, unused_genes, network_as_list, genes_non_sort = ImportBooleanModel(
                            genes_list_filename,
                            network_filename)


                window_visu = layoutBooleanModelVisu()

                active_1, active_2, active_3, active_4, active_Canva, active_Canva_2, active_Canva_3 = True, False, False, False, False, False,False


                run = True
                FigOn = False
                FigOn_2 = False
                movie_1 = False
                movie_2 = False
                movie_load = False

                layout_graph_drawing = [
                    'circular_layout',
                    'kamada_kawai_layout',
                    'random_layout',
                    'shell_layout',
                    'spring_layout',
                    'spectral_layout',
                    'planar_layout',
                    'fruchterman_reingold_layout',
                    'spiral_layout']

                layout_color_drawing = ["blue", "orange", "green", "red", "purple", "brown", "pink", "grey", "olive",
                                        "cyan", "black"]

                state_none = -1
                layout_selected_previous, layout_selected_previous_2 , layout_selected_previous_3 = None, None , None
                activate_gene_color_previous, activate_gene_color_previous_2, activate_gene_color_previous_3 = None, None , None
                inactivate_gene_color_previous, inactivate_gene_color_previous_2 , inactivate_gene_color_previous_3 = None, None , None
                activate_interaction_color_previous, activate_interaction_color_previous_2 , activate_interaction_color_previous_3 = None, None , None
                inactivate_interaction_color_previous, inactivate_interaction_color_previous_2 , inactivate_interaction_color_previous_3= None, None , None
                width_interaction_previous, width_interaction_previous_2 , width_interaction_previous_3 = None, None , None
                genes_selected_visu_previous, genes_selected_visu_previous_2 , genes_selected_visu_previous_3 = None, None , None

                while True :
                    for i in range(7):
                        if active_1 :
                            event_visu, values_visu = window_visu.read(timeout=100)

                        # catch all parameters from the GUI
                            genes_selected = values_visu[0]
                            interactions_selected = values_visu[1]
                            boolean_model_selected = values_visu[2]
                            boundary_model_selected = values_visu[3]
                            initial_state_selected = values_visu[4]
                            all_initial_states_bool_visu = values_visu[5]
                            subset_initial_states_bool_visu = values_visu[6]
                            number_initial_states = values_visu[7]
                            KO_type_selected = values_visu[8]
                            source_gene_add = values_visu[12]
                            interaction_add = values_visu[13]
                            target_gene_add = values_visu[14]
                            CSV_element_add = values_visu[15]
                            load_saved_file = values_visu[16]
                            if KO_type_selected != 'none':
                                KO_genes_selected = values_visu[9]
                                KO_genes_selected = KO_genes_selected.rsplit(',')
                            else:
                                KO_genes_selected = ['foo']
                            OA_type_selected = values_visu[10]
                            if OA_type_selected != 'none':
                                OA_genes_selected = values_visu[11]
                                OA_genes_selected = OA_genes_selected.rsplit(',')
                            else:
                                OA_genes_selected = ['foo']


                            if event_visu in (sg.WIN_CLOSED, 'Exit'):
                                run = Falsef
                                break

                            if event_visu == 'Add element':
                                source_gene_list, interaction_list, target_gene_list = catchGUIElement(source_gene_add, interaction_add, target_gene_add)
                                genes_names_list, network_dictionary, network_as_list = addElement(network_dictionary, genes_names_list,
                                                                                                   network_as_list, source_gene_list, interaction_list,target_gene_list)
                            if event_visu == 'Add element from CSV':
                                check, error_path = checkPath(CSV_element_add)
                                check_format_load = checkLoadElement(CSV_element_add)
                                if check == False :
                                    sg.popup_error("File doesn't exist in specified folder")
                                if check == True:
                                    check_format_load = checkLoadElement(CSV_element_add)
                                    if check_format_load == False :
                                        sg.popup_error("File format is wrong")
                                    if check_format_load == True :
                                        source_gene_list, interaction_list, target_gene_list = addElementfromCSV(CSV_element_add)
                                        genes_names_list, network_dictionary, network_as_list = addElement(network_dictionary, genes_names_list,
                                                                                                       network_as_list, source_gene_list, interaction_list,target_gene_list)
                            if event_visu == "Load" and not active_4 :
                                check, error_path = checkPath(load_saved_file)


                                if check == False :
                                    sg.popup_error("File doesn't exist in specified folder")
                                if check == True :
                                    check_format_savednetwork = checkSavedNetwork(load_saved_file)
                                    if check_format_savednetwork == False :
                                        sg.popup_error("Network format is wrong")
                                         if check_format_savednetwork == True :
                                            active_4 = True
                                            interaction_table, node_table , list_panel_loading  = openData(load_saved_file)
                                            window_4 = layoutVisuGraph(list_panel_loading, layout_graph_drawing, layout_color_drawing, "Loaded Graph")

                            if event_visu == 'Run HELIOS' and not active_2 :   # only run if not already showing a window2
                                active_2 = True

                                print("genes selectionnes : ", genes_selected)
                                if all_initial_states_bool_visu:
                                    flow, stable, start, stable_states, initial_states, genes_names, data, network, time = RunBooleanModelVisu(
                                        genes_names=genes_names_list, genes_network=network_dictionary, initial_state_number='all',
                                        initial_state_choice=initial_state_selected,
                                        model=boolean_model_selected, stimulus=boundary_model_selected,
                                        initial_state_genes=genes_selected,
                                        KO_genes=KO_genes_selected, OA_genes=OA_genes_selected)

                                    resMod(genes_names_list, network_dictionary, start, flow, stable, genes_list_filename,
                                           network_filename,
                                           genes_names, KO_genes_selected, OA_genes_selected, boolean_model_selected,
                                           boundary_model_selected, network, initial_states, stable_states, data)

                                elif subset_initial_states_bool_visu:
                                    flow, stable, start, stable_states, initial_states, genes_names, data, network, time = RunBooleanModelVisu(
                                        genes_names=genes_names_list, genes_network=network_dictionary,
                                        initial_state_number=number_initial_states, initial_state_choice=initial_state_selected,
                                        model=boolean_model_selected, stimulus=boundary_model_selected,
                                        initial_state_genes=genes_selected,
                                        KO_genes=KO_genes_selected, OA_genes=OA_genes_selected)

                                else:
                                    sg.Popup(
                                        'Please select value for number of initial states ( <<all>> or enter numerical value ) and run PYTHONIS again',
                                        no_titlebar=True, background_color='#343434')

                                list_panel = createListPanelGraph(flow)
                                window_2 = layoutVisuGraph(list_panel, layout_graph_drawing, layout_color_drawing, "Boolean analysis - Helios")

                            if event_visu == 'Run HELIOS 2' and not active_3:
                                active_3 = True
                                if all_initial_states_bool_visu:
                                    flow, stable, start, stable_states, initial_states, genes_names, data, network, time = RunBooleanModelVisu(
                                        genes_names=genes_names_list, genes_network=network_dictionary, initial_state_number='all',
                                        initial_state_choice=initial_state_selected,
                                        model=boolean_model_selected, stimulus=boundary_model_selected,
                                        initial_state_genes=genes_selected,
                                        KO_genes=KO_genes_selected, OA_genes=OA_genes_selected)

                                    resMod(genes_names_list, network_dictionary, start, flow, stable, genes_list_filename,
                                           network_filename,
                                           genes_names, KO_genes_selected, OA_genes_selected, boolean_model_selected,
                                           boundary_model_selected, network, initial_states, stable_states, data)

                                elif subset_initial_states_bool_visu:
                                    flow, stable, start, stable_states, initial_states, genes_names, data, network, time = RunBooleanModelVisu(
                                        genes_names=genes_names_list, genes_network=network_dictionary,
                                        initial_state_number=number_initial_states, initial_state_choice=initial_state_selected,
                                        model=boolean_model_selected, stimulus=boundary_model_selected,
                                        initial_state_genes=genes_selected,
                                        KO_genes=KO_genes_selected, OA_genes=OA_genes_selected)

                                else:
                                    sg.Popup(
                                        'Please select value for number of initial states ( <<all>> or enter numerical value ) and run PYTHONIS again',
                                        no_titlebar=True, background_color='#343434')

                                list_panel = createListPanelGraph(flow)
                                window_3 = layoutVisuGraph(list_panel, layout_graph_drawing, layout_color_drawing, "Boolean analysis - Helios 2")

                        if active_2:
                            event_2, values_2 = window_2.read(timeout = 100)
                            genes_selected_visu = values_2[0]
                            graph_selected = values_2[1]
                            layout_selected = values_2[2]
                            activate_gene_color = values_2[3]
                            inactivate_gene_color = values_2[4]
                            activate_interaction_color = values_2[5]
                            inactivate_interaction_color = values_2[6]
                            width_interaction = values_2[7]
                            name_saved_file = values_2[8]
                            name_saved_movie = values_2[9]
                            if event_2 in (sg.WIN_CLOSED, 'Exit'):
                                active_2 = False
                                window_2.close()


                            if event_2 == 'Save gene activity':
                                drawStateActivationGraph(genes_selected_visu, flow, genes_names_list)

                            if event_2 == 'Launch visualization':
                                active_Canva = True
                                layout_graph = [[sg.Canvas(size=(800,800), key='-CANVAS2-'), sg.Button("Save as PNG")]]
                                window_graph = sg.Window('Interaction Graph',
                                                         layout_graph, finalize=True)

                                fig, G = drawGraph(genes_names_list, network_as_list, flow, graph_selected,
                                                   layout_selected,
                                                   activate_gene_color, inactivate_gene_color, activate_interaction_color,
                                                   inactivate_interaction_color,
                                                   width_interaction, genes_selected_visu, state_none)
                                fig_canvas_agg = draw_figure(window_graph['-CANVAS2-'].TKCanvas, fig)
                                canvas_elem = window_graph['-CANVAS2-']
                                canvas = canvas_elem.TKCanvas
                                event_graph, values_graph = window_graph.read()
                                if event_graph == "Save as PNG" :
                                    savePNG(fig, graph_selected, 2)
                                window_graph.close()
                                delete_figure_agg(fig_canvas_agg)
                            if event_2 == "Save graph":
                                saveData(network_as_list, flow, genes_names_list, name_saved_file)


                            if event_2 == "Save as video" :
                                folder_png = createFolderSave()
                                for state in list_panel :
                                    fig, G = drawGraph(genes_names_list, network_as_list, flow, state,
                                                       layout_selected,
                                                       activate_gene_color, inactivate_gene_color, activate_interaction_color,
                                                       inactivate_interaction_color,
                                                       width_interaction, genes_selected_visu, state)
                                    # savePNG(fig, state)
                                createVideo(folder_png, name_saved_movie)
                                deleteFolder(folder_png)

                            if event_2 == "Display dynamic view":
                                if layout_selected != layout_selected_previous or activate_gene_color != activate_gene_color_previous or inactivate_gene_color != inactivate_gene_color_previous or activate_interaction_color != activate_interaction_color_previous or inactivate_interaction_color != inactivate_interaction_color_previous or width_interaction != width_interaction_previous or genes_selected_visu != genes_selected_visu_previous :
                                    layout_selected_previous = layout_selected
                                    activate_gene_color_previous = activate_gene_color
                                    inactivate_gene_color_previous = inactivate_gene_color
                                    activate_interaction_color_previous = activate_interaction_color
                                    inactivate_interaction_color_previous = inactivate_interaction_color
                                    width_interaction_previous = width_interaction
                                    genes_selected_visu_previous = genes_selected_visu
                                    movie_1 = False
                                if movie_1 == False :
                                    folder_png = createFolderSave()
                                    for state in list_panel :
                                        fig, G = drawGraph(genes_names_list, network_as_list, flow, state,
                                                           layout_selected,
                                                           activate_gene_color, inactivate_gene_color, activate_interaction_color,
                                                           inactivate_interaction_color,
                                                           width_interaction, genes_selected_visu, state)
                                    createVideo(folder_png, "Helios_movie_1.mp4")
                                    deleteFolder(folder_png)
                                    movie_1 = True
                                vidFile = cv.VideoCapture("Helios_movie_1.mp4")
                                # ---===--- Get some Stats --- #
                                num_frames = vidFile.get(cv.CAP_PROP_FRAME_COUNT)
                                fps = vidFile.get(cv.CAP_PROP_FPS)
                                sg.theme('Black')

                                # ---===--- define the window layout --- #
                                layout = [[sg.Image(filename='', key='-image-')],
                                          [sg.Slider(range=(0, num_frames),
                                                     size=(60, 10), orientation='h', key='-slider-')],
                                          [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]]

                                # create the window and show it without the plot
                                window_view = sg.Window('Dynamic View', layout, no_titlebar=False, location=(0, 0))

                                # locate the elements we'll be updating. Does the search only 1 time
                                image_elem = window_view['-image-']
                                slider_elem = window_view['-slider-']

                                # ---===--- LOOP through video file by frame --- #
                                cur_frame = 0
                                while vidFile.isOpened():
                                    event_view, values_view = window_view.read(timeout=0)
                                    if event_view in ('Exit', None):
                                        break
                                    ret, frame = vidFile.read()
                                    if not ret:  # if out of data stop looping
                                        break
                                    # if someone moved the slider manually, the jump to that frame
                                    if int(values_view['-slider-']) != cur_frame - 1:
                                        cur_frame = int(values_view['-slider-'])
                                        vidFile.set(cv.CAP_PROP_POS_FRAMES, cur_frame)
                                    slider_elem.update(cur_frame)
                                    cur_frame += 1

                                    imgbytes = cv.imencode('.png', frame)[1].tobytes()  # ditto
                                    image_elem.update(data=imgbytes)

                        ################################################################################################################################################
                        if active_3:
                            event_3, values_3 = window_3.read(timeout = 100)
                            genes_selected_visu_2 = values_3[0]
                            graph_selected_2 = values_3[1]
                            layout_selected_2 = values_3[2]
                            activate_gene_color_2 = values_3[3]
                            inactivate_gene_color_2 = values_3[4]
                            activate_interaction_color_2 = values_3[5]
                            inactivate_interaction_color_2 = values_3[6]
                            width_interaction_2 = values_3[7]
                            name_saved_file_2 = values_3[8]
                            name_saved_movie_2 = values_3[9]
                            if event_3 in (sg.WIN_CLOSED, 'Exit'):
                                active_3 = False
                                window_3.close()


                            if event_3 == 'Save gene activity':
                                drawStateActivationGraph(genes_selected_visu_2, flow, genes_names_list)

                            if event_3 == 'Launch visualization':

                                active_Canva_2 = True
                                layout_graph_2 = [[sg.Canvas(size=(640, 480), key='-CANVAS-'), sg.Button("Save as PNG")]]
                                window_graph_2 = sg.Window('Interaction Graph',
                                                         layout_graph_2, finalize=True)
                                fig_2, G = drawGraph(genes_names_list, network_as_list, flow, graph_selected_2,
                                                   layout_selected_2,
                                                   activate_gene_color_2, inactivate_gene_color_2, activate_interaction_color_2,
                                                   inactivate_interaction_color_2,
                                                   width_interaction_2, genes_selected_visu_2, state_none)
                                # add the plot to the window
                                fig_canvas_agg = draw_figure(window_graph_2['-CANVAS-'].TKCanvas, fig_2)
                                canvas_elem = window_graph_2['-CANVAS-']
                                canvas = canvas_elem.TKCanvas
                                event_graph_2, values_graph_2 = window_graph_2.read()
                                if event_graph_2 == "Save as PNG" :
                                    savePNG(fig_2, graph_selected_2, 2)
                                window_graph_2.close()
                                delete_figure_agg(fig_canvas_agg)


                            if event_3 == "Save graph":
                                saveData(network_as_list, flow, genes_names_list, name_saved_file_2)

                            if event_3 == "Save as video" :
                                folder_png = createFolderSave()
                                for state_2 in list_panel :
                                    fig_2, G = drawGraph(genes_names_list, network_as_list, flow, state_2,
                                                       layout_selected_2,
                                                       activate_gene_color_2, inactivate_gene_color_2, activate_interaction_color_2,
                                                       inactivate_interaction_color_2,
                                                       width_interaction_2, genes_selected_visu_2, state_2)
                                createVideo(folder_png, name_saved_movie_2)
                                deleteFolder(folder_png)

                            if event_3 == "Display dynamic view":
                                if layout_selected_2 != layout_selected_previous_2 or activate_gene_color_2 != activate_gene_color_previous_2 or inactivate_gene_color_2 != inactivate_gene_color_previous_2 or activate_interaction_color_2 != activate_interaction_color_previous_2 or inactivate_interaction_color_2 != inactivate_interaction_color_previous_2 or width_interaction_2 != width_interaction_previous_2 or genes_selected_visu_2 != genes_selected_visu_previous_2 :
                                    layout_selected_previous_2 = layout_selected_2
                                    activate_gene_color_previous_2 = activate_gene_color_2
                                    inactivate_gene_color_previous_2 = inactivate_gene_color_2
                                    activate_interaction_color_previous_2 = activate_interaction_color_2
                                    inactivate_interaction_color_previous_2 = inactivate_interaction_color_2
                                    width_interaction_previous_2 = width_interaction_2
                                    genes_selected_visu_previous_2 = genes_selected_visu_2
                                    movie_2 = False
                                if movie_2 == False :
                                    folder_png = createFolderSave()
                                    for state_2 in list_panel :
                                        fig_2, G = drawGraph(genes_names_list, network_as_list, flow, state_2,
                                                           layout_selected_2,
                                                           activate_gene_color_2, inactivate_gene_color_2, activate_interaction_color_2,
                                                           inactivate_interaction_color_2,
                                                           width_interaction_2, genes_selected_visu_2, state_2)
                                    createVideo(folder_png, "Helios_movie_2.mp4")
                                    deleteFolder(folder_png)
                                    movie_2 = True

                                vidFile = cv.VideoCapture("Helios_movie_2.mp4")
                                # ---===--- Get some Stats --- #
                                num_frames = vidFile.get(cv.CAP_PROP_FRAME_COUNT)
                                fps = vidFile.get(cv.CAP_PROP_FPS)
                                sg.theme('Black')
                                # ---===--- define the window layout --- #
                                layout = [[sg.Image(filename='', key='-image-')],
                                          [sg.Slider(range=(0, num_frames),
                                                     size=(60, 10), orientation='h', key='-slider-')],
                                          [sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]]

                                # create the window and show it without the plot
                                window_view_2 = sg.Window('Dynamic View', layout, no_titlebar=False, location=(0, 0))

                                # locate the elements we'll be updating. Does the search only 1 time
                                image_elem = window_view_2['-image-']
                                slider_elem = window_view_2['-slider-']
                                # ---===--- LOOP through video file by frame --- #
                                cur_frame = 0
                                while vidFile.isOpened():
                                    event_view_2, values_view_2 = window_view_2.read(timeout=0)
                                    if event_view_2 in ('Exit', None):
                                        break
                                    ret, frame = vidFile.read()
                                    if not ret:  # if out of data stop looping
                                        break
                                    # if someone moved the slider manually, the jump to that frame
                                    if int(values_view_2['-slider-']) != cur_frame - 1:
                                        cur_frame = int(values_view_2['-slider-'])
                                        vidFile.set(cv.CAP_PROP_POS_FRAMES, cur_frame)
                                    slider_elem.update(cur_frame)
                                    cur_frame += 1

                                    imgbytes = cv.imencode('.png', frame)[1].tobytes()  # ditto
                                    image_elem.update(data=imgbytes)
                        ################################################################################################################################################
                        if active_4:
                            event_4, values_4 = window_4.read(timeout = 100)
                            genes_selected_visu_3 = values_4[0]
                            graph_selected_3 = values_4[1]
                            layout_selected_3 = values_4[2]
                            activate_gene_color_3 = values_4[3]
                            inactivate_gene_color_3 = values_4[4]
                            activate_interaction_color_3 = values_4[5]
                            inactivate_interaction_color_3 = values_4[6]
                            width_interaction_3 = values_4[7]
                            name_saved_file_3 = values_4[8]
                            name_saved_movie_3 = values_4[9]
                            if event_4 in (sg.WIN_CLOSED, 'Exit'):
                                active_4 = False
                                window_4.close()

                            if event_4 == 'Save gene activity':
                                drawStateActivationGraph(genes_selected_visu_3, flow, genes_names_list)

                            if event_4 == 'Launch visualization':
                                active_Canva_3 = True
                                layout_graph_3 = [[sg.Canvas(size=(640, 480), key='-CANVAS-'), sg.Button("Save as PNG")]]
                                window_graph_3 = sg.Window('Interaction Graph',
                                                         layout_graph_3, finalize=True)

                                fig_3, G = drawLoadGraph(layout_selected_3, interaction_table, node_table, graph_selected_3, activate_gene_color_3,
                                                  inactivate_gene_color_3, activate_interaction_color_3, inactivate_interaction_color_3, width_interaction_3, genes_selected_visu_3, state_none)
                                # add the plot to the window
                                fig_canvas_agg = draw_figure(window_graph_3['-CANVAS-'].TKCanvas, fig_3)
                                canvas_elem = window_graph_3['-CANVAS-']
                                canvas = canvas_elem.TKCanvas
                                event_graph_3, values_graph_3 = window_graph_3.read()
                                if event_graph_3 == "Save as PNG" :
                                    savePNG(fig_3, graph_selected_3, 2)
                                window_graph_3.close()
                                delete_figure_agg(fig_canvas_agg)

                            if event_4 == "Save as video" :
                                folder_png = createFolderSave()
                                for state_3 in list_panel_loading :
                                    fig_3, G = drawLoadGraph(layout_selected_3, interaction_table, node_table, state_3, activate_gene_color_3,
                                                      inactivate_gene_color_3, activate_interaction_color_3, inactivate_interaction_color_3, width_interaction_3, genes_selected_visu_3, state_3)
                                createVideo(folder_png, name_saved_movie_3)
                                deleteFolder(folder_png)

                            if event_4 == "Display dynamic view":
                                if layout_selected_3 != layout_selected_previous_3 or activate_gene_color_3 != activate_gene_color_previous_3 or inactivate_gene_color_3 != inactivate_gene_color_previous_3 or activate_interaction_color_3 != activate_interaction_color_previous_3 or inactivate_interaction_color_3 != inactivate_interaction_color_previous_3 or width_interaction_3 != width_interaction_previous_3 or genes_selected_visu_3 != genes_selected_visu_previous_3 :
                                    layout_selected_previous_3 = layout_selected_3
                                    activate_gene_color_previous_3 = activate_gene_color_3
                                    inactivate_gene_color_previous_3 = inactivate_gene_color_3
                                    activate_interaction_color_previous_3 = activate_interaction_color_3
                                    inactivate_interaction_color_previous_3 = inactivate_interaction_color_3
                                    width_interaction_previous_3 = width_interaction_3
                                    genes_selected_visu_previous_3 = genes_selected_visu_3
                                    movie_load = False
                                if movie_load == False :
                                    folder_png = createFolderSave()
                                    for state_3 in list_panel_loading :
                                        fig_3, G = drawLoadGraph(layout_selected_3, interaction_table, node_table, state_3, activate_gene_color_3,
                                                          inactivate_gene_color_3, activate_interaction_color_3, inactivate_interaction_color_3, width_interaction_3, genes_selected_visu_3, state_3)

                                    createVideo(folder_png, "load_graph_movie.mp4")
                                    deleteFolder(folder_png)
                                    movie_load = True

                                ################
                                vidFile = cv.VideoCapture("load_graph_movie.mp4")
                                # ---===--- Get some Stats --- #
                                num_frames = vidFile.get(cv.CAP_PROP_FRAME_COUNT)
                                fps = vidFile.get(cv.CAP_PROP_FPS)
                                sg.theme('Black')
                                # ---===--- define the window layout --- #
                                layout = [[sg.Image(filename='', key='-image-')],
                                          [sg.Slider(range=(0, num_frames),
                                                     size=(60, 10), orientation='h', key='-slider-')]]

                                # create the window and show it without the plot
                                window_view_2 = sg.Window('Dynamic View', layout, no_titlebar=False, location=(0, 0))

                                # locate the elements we'll be updating. Does the search only 1 time
                                image_elem = window_view_2['-image-']
                                slider_elem = window_view_2['-slider-']
                                # ---===--- LOOP through video file by frame --- #
                                cur_frame = 0
                                while vidFile.isOpened():
                                    event_view_2, values_view_2 = window_view_2.read(timeout=0)
                                    if event_view_2 in ('Exit', None):
                                        break
                                    ret, frame = vidFile.read()
                                    if not ret:  # if out of data stop looping
                                        break
                                    # if someone moved the slider manually, the jump to that frame
                                    if int(values_view_2['-slider-']) != cur_frame - 1:
                                        cur_frame = int(values_view_2['-slider-'])
                                        vidFile.set(cv.CAP_PROP_POS_FRAMES, cur_frame)
                                    slider_elem.update(cur_frame)
                                    cur_frame += 1

                                    imgbytes = cv.imencode('.png', frame)[1].tobytes()  # ditto
                                    image_elem.update(data=imgbytes)

                    if run == False:
                        break
