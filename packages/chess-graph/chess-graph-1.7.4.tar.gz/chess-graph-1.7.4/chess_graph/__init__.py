from chess_graph import chart

def graph(database, depth=5, shade = True, fragmentation_percentage=0.0032, should_defragment=False, custom_branching=False, should_download = False, download_format = 'png', download_name = 'fig1', color = 'both', name = ''):

    return chart.graph(database, depth, shade, fragmentation_percentage, should_defragment, custom_branching, should_download, download_format, download_name, color, name)
