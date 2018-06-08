import json
import csv
from operator import itemgetter
from itertools import islice
import cv2
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

RECIPE_id = 0
RECIPE_desc = 1
RECIPE_trig_chan_id = 2
RECIPE_trig_chan_title = 3
RECIPE_trig_id = 4
RECIPE_trig_title = 5
RECIPE_act_chan_id = 6
RECIPE_act_chan_title = 7
RECIPE_act_id = 8
RECIPE_act_title = 9
RECIPE_addCount = 10
RECIPE_url = 11
RECIPE_violation = 12



trig_chan_id_stat = 2
act_chan_id_stat = 6

def classify_recipe_data():
    write_header_to_file()
    d={}
    lst=[]
    id =0
    print("Started")
    file = open("recipes.json", "r")
    for line in file:
        try:
            d=json.loads(line)
            d['id']=id

            if d['desc'] == "":
                d['desc'] = 'not available'
            desc = d['desc'].encode('utf-8')

            trig_chan_id = d['triggerChannelId']
            trig_chan_title = d['triggerChannelTitle'].encode('utf-8')
            trig_id = d['triggerId']
            trig_title = d['triggerTitle'].encode('utf-8')
            act_chan_id = d['actionChannelId']
            act_chan_title = d['actionChannelTitle'].encode('utf-8')
            act_id = d['actionId']
            act_title = d['actionTitle'].encode('utf-8')

            addCount = str(d['addCount'])
            if 'k' in addCount:
                try:
                    addCount = float(addCount.replace('k', '')) * 1000
                    d['addCount'] = addCount
                except:
                    print("exception occur")
                    print(addCount)
                    pass

            url = d['url'].encode('utf-8')
            violation = 'x'
            d['violation'] = violation
            write_data_to_file(id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id, act_chan_title, act_id, act_title, addCount, url, violation)
            id += 1
            # channel[trig_chan_title] += 1

            lst.append(d)
        except Exception as e:
            print("Exception Occur "+ desc +str(e))
            pass

    print("Finished")

    return lst


def get_most_popular_recipe(lst, top):

    write_most_used_recipe_by_addcount_header_to_file()
    mod_lst=sorted(lst, key = lambda d: (int(d['addCount'])))
    iterator = mod_lst[-top:]
    most_lst = []
    for d in iterator:
        # print(str(d['addCount'])+"  "+str(d['desc'].encode('utf-8')))
        most_lst.append(d)

        id = d['id']
        desc = d['desc'].encode('utf-8')
        trig_chan_id = d['triggerChannelId']
        trig_chan_title = d['triggerChannelTitle'].encode('utf-8')
        trig_id = d['triggerId']
        trig_title = d['triggerTitle'].encode('utf-8')
        act_chan_id = d['actionChannelId']
        act_chan_title = d['actionChannelTitle'].encode('utf-8')
        act_id = d['actionId']
        act_title = d['actionTitle'].encode('utf-8')
        addCount = str(d['addCount'])
        url = d['url'].encode('utf-8')
        violation = d['violation']

        write_most_used_recipe_by_addcount(id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id, act_chan_title, act_id, act_title, addCount, url, violation)

    return most_lst

def search_by_channel_id(lst, channel_id):

    pop_lst=[]
    for item in lst:
        if item['triggerChannelId'] == channel_id:
            pop_lst.append(item)
    return pop_lst


def write_header_to_file():
    outfile = open("./stat.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(['id', 'desc', 'trig_chan_id', 'trig_chan_title', 'trig_id', 'trig_title', 'act_chan_id', 'act_chan_title', 'act_id', 'act_title', 'addCount', 'url', 'violation'])
    outfile.close()

def write_selected_recipe_by_channel_header_to_file():
    outfile = open("./stat_selected_recipe_channel.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(['id', 'desc', 'trig_chan_id', 'trig_chan_title', 'trig_id', 'trig_title', 'act_chan_id', 'act_chan_title', 'act_id', 'act_title', 'addCount', 'url', 'violation'])
    outfile.close()

def write_most_used_recipe_by_addcount_header_to_file():
    outfile = open("./stat_most_used_recipe.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(['id', 'desc', 'trig_chan_id', 'trig_chan_title', 'trig_id', 'trig_title', 'act_chan_id', 'act_chan_title', 'act_id', 'act_title', 'addCount', 'url', 'violation'])
    outfile.close()

def write_header_channel_file():
    outfile = open("./stat_channel.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(["id", "chan_id", "chan_title", "chan_url", "consideration"])
    outfile.close()

def write_header_interaction_chain():
    outfile = open("./stat_intearaction_chain.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(["id","key","value","violation"])
    outfile.close()

def write_channel_data_to_file(id, chan_id, chan_title, chan_url, consideration):
    outfile = open("./stat_channel.csv", "a")
    writer = csv.writer(outfile)
    writer.writerow([id, chan_id, chan_title, chan_url, consideration])
    outfile.close()

def write_data_to_file(id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id, act_chan_title, act_id, act_title, addCount, url, violation):
    outfile = open("./stat.csv", "a")
    writer = csv.writer(outfile)
    writer.writerow([id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id, act_chan_title, act_id,act_title, addCount, url, violation])
    outfile.close()

def write_selected_recipe_by_channel(id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id, act_chan_title, act_id, act_title, addCount, url, violation):
    outfile = open("./stat_selected_recipe_channel.csv", "a")
    writer = csv.writer(outfile)
    writer.writerow([id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id, act_chan_title, act_id,act_title, addCount, url, violation])
    outfile.close()

def write_most_used_recipe_by_addcount(id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id, act_chan_title, act_id, act_title, addCount, url, violation):
    outfile = open("./stat_most_used_recipe.csv", "a")
    writer = csv.writer(outfile)
    writer.writerow([id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id, act_chan_title, act_id,act_title, addCount, url, violation])
    outfile.close()

def write_interaction_chain(id, key, value, violation):
    outfile = open("./stat_intearaction_chain.csv", "a")
    writer = csv.writer(outfile)
    writer.writerow([id,key,value,violation])
    outfile.close()

def classify_channel_data():
    write_header_channel_file()
    file = open("channelList.json", "r")
    lst=[]
    id =0
    print("Started")
    for line in file:
        try:
            d=json.loads(line)
            d['id']=id
            chan_id = d['channelId']
            chan_title = d['channelName'].encode('utf-8')
            chan_url = d['channelUrl'].encode('utf-8')

            consideration = 'x'
            write_channel_data_to_file(id, chan_id, chan_title, chan_url, consideration)
            id += 1

            lst.append(d)
        except Exception as e:
            print("Exception Occur ")
            pass

    print("Finished")

    return lst

def get_selected_channel_list():
    file = open("stat_channel.csv", "r")
    lst = []
    for line in file:
        str = line.split(",")
        if str[4].strip() == 'o':
            lst.append(str[1])
    return lst

def get_all_channel_list():
    file = open("stat_channel.csv", "r")
    lst = []
    for line in file:
        line=line.strip()
        lst.append(line)
    file.close()
    return lst

def get_recipe_by_channel(lst):
    write_selected_recipe_by_channel_header_to_file()
    file = open("./stat.csv", "r")
    rcp_lst=[]
    for line in file:
        line=line.strip()
        str = line.split(",")
        # print str
        for item in lst:
            try:
                if item == str[trig_chan_id_stat].strip():
                    rcp_lst.append(line)
                elif item == str[act_chan_id_stat].strip():
                    rcp_lst.append(line)
            except:
                pass

    for l in rcp_lst:
        l=l.strip()
        str = l.split(",")

        id = str[RECIPE_id]
        desc = str[RECIPE_desc]
        trig_chan_id = str[RECIPE_trig_chan_id]
        trig_chan_title = str[RECIPE_trig_chan_title]
        trig_id = str[RECIPE_trig_id]
        trig_title = str[RECIPE_trig_title]
        act_chan_id = str[RECIPE_act_chan_id]
        act_chan_title = str[RECIPE_act_chan_title]
        act_id = str[RECIPE_act_id]
        act_title = str[RECIPE_act_title]
        addCount = str[RECIPE_addCount]
        url = str[RECIPE_url]
        violation = str[RECIPE_violation]

        write_selected_recipe_by_channel(id, desc, trig_chan_id, trig_chan_title, trig_id, trig_title, act_chan_id,
                                         act_chan_title, act_id, act_title, addCount, url, violation)
    return rcp_lst


def generate_interaction_chain():
    write_header_interaction_chain()
    file = open("./stat_selected_recipe_channel.csv", "r")
    lst = []
    d = dict()
    index =0
    violation = 'x'
    for line in file:
        line = line.strip()
        lst.append(line)


    for item in lst:
        str = item.split(",")
        id = str[RECIPE_id]

        trig_chan_id = str[RECIPE_trig_chan_id]
        trig_chan_title = str[RECIPE_trig_chan_title]
        trig_title = str[RECIPE_trig_title]

        act_chan_id = str[RECIPE_act_chan_id]
        act_chan_title = str[RECIPE_act_chan_title]
        act_title = str[RECIPE_act_title]

        dict_key = trig_chan_id +"-"+trig_chan_title+"-"+trig_title
        dict_value =  act_chan_id + "-" + act_chan_title + "-" +act_title

        #preventing duplicate
        if dict_key in d:
            continue

        d[dict_key] = [dict_value]

        for item2 in lst:
            str2 = item2.split(",")
            id2 = str2[RECIPE_id]
            if id != id2:

                trig_chan_id_2 = str2[RECIPE_trig_chan_id]
                trig_chan_title_2 = str2[RECIPE_trig_chan_title]
                trig_title_2 = str2[RECIPE_trig_title]

                act_chan_id_2 = str2[RECIPE_act_chan_id]
                act_chan_title_2 = str2[RECIPE_act_chan_title]
                act_title_2 = str2[RECIPE_act_title]

                if trig_chan_id == trig_chan_id_2 and trig_title == trig_title_2:
                    dict_value = act_chan_id_2 + "-" + act_chan_title_2+ "-" + act_title_2
                    d[dict_key].append(dict_value)

        write_interaction_chain(index, dict_key, d[dict_key], violation)
        index +=1

def write_interaction_chain_between_channels_header_to_file():
    outfile = open("./stat_intearaction_chain_between_channel.csv", "w")
    writer = csv.writer(outfile)
    writer.writerow(["key","value"])
    outfile.close()

def write_interaction_chain_between_channels(key, value):
    outfile = open("./stat_intearaction_chain_between_channel.csv", "a")
    writer = csv.writer(outfile)
    writer.writerow([key,value])
    outfile.close()

def generate_interaction_chain_between_channels():

    write_interaction_chain_between_channels_header_to_file()
    channels = get_all_channel_list()
    ids={}
    for chnl in channels:
        str = chnl.split(",")
        ids[str[1]] = [str[2]]

    print(ids)


    file = open("./stat.csv", "r")
    for line in file:
        try:
            line = line.strip()
            str = line.split(",")
            trig_chan_id = str[RECIPE_trig_chan_id]

            act_chan_id = str[RECIPE_act_chan_id]
            act_chan_title = str[RECIPE_act_chan_title].encode('utf-8')
            ids[trig_chan_id].append(act_chan_title)
        except Exception as e:
            pass
            # print(e)

    for (key,value) in ids.items():
        write_interaction_chain_between_channels(key, value)
    file.close()
    return ids


# def drawGraph():
#     assert float(cv2.__version__.rsplit('.', 1)[0]) >= 3, 'OpenCV version 3 or newer required.'
#
#     K = np.array([[689.21, 0., 1295.56],
#                   [0., 690.48, 942.17],
#                   [0., 0., 1.]])
#
#     # zero distortion coefficients work well for this image
#     D = np.array([0., 0., 0., 0.])
#
#     # use Knew to scale the output
#     Knew = K.copy()
#     Knew[(0, 1), (0, 1)] = 0.4 * Knew[(0, 1), (0, 1)]
#
#     img = cv2.imread('fisheye_sample.jpg')
#     img_undistorted = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)
#     cv2.imwrite('fisheye_sample_undistorted.jpg', img_undistorted)
#     cv2.imshow('undistorted', img_undistorted)
#     cv2.waitKey()

# def drawGraph():
#
#     G = nx.random_geometric_graph(200, 0.125)
#     pos = nx.get_node_attributes(G, 'pos')
#
#     dmin = 1
#     ncenter = 0
#     for n in pos:
#         x, y = pos[n]
#         d = (x - 0.5) ** 2 + (y - 0.5) ** 2
#         if d < dmin:
#             ncenter = n
#             dmin = d
#
#     p = nx.single_source_shortest_path_length(G, ncenter)
#
#     edge_trace = Scatter(
#         x=[],
#         y=[],
#         line=Line(width=0.5, color='#888'),
#         hoverinfo='none',
#         mode='lines')
#
#     for edge in G.edges():
#         x0, y0 = G.node[edge[0]]['pos']
#         x1, y1 = G.node[edge[1]]['pos']
#         edge_trace['x'] += [x0, x1, None]
#         edge_trace['y'] += [y0, y1, None]
#
#     node_trace = Scatter(
#         x=[],
#         y=[],
#         text=[],
#         mode='markers',
#         hoverinfo='none',
#         marker=Marker(
#             showscale=True,
#             # colorscale options
#             # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
#             # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
#             colorscale='YIGnBu',
#             reversescale=True,
#             color=[],
#             size=10,
#             colorbar=dict(
#                 thickness=15,
#                 title='Node Connections',
#                 xanchor='left',
#                 titleside='right'
#             ),
#             line=dict(width=2)))
#
#     for node in G.nodes():
#         x, y = G.node[node]['pos']
#         node_trace['x'].append(x)
#         node_trace['y'].append(y)
#
#     for node, adjacencies in enumerate(G.adjacency_list()):
#         node_trace['marker']['color'].append(len(adjacencies))
#         node_info = '# of connections: ' + str(len(adjacencies))
#         node_trace['text'].append(node_info)
#
#     fig = Figure(data=Data([edge_trace, node_trace]),
#                  layout=Layout(
#                      title='<br>Network graph made with Python',
#                      titlefont=dict(size=16),
#                      showlegend=False,
#                      hovermode='closest',
#                      margin=dict(b=20, l=5, r=5, t=40),
#                      annotations=[dict(
#                          text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
#                          showarrow=False,
#                          xref="paper", yref="paper",
#                          x=0.005, y=-0.002)],
#                      xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
#                      yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
#
#     py.iplot(fig, filename='networkx')

# def drawGraph():
#     chnls = generate_interaction_chain_between_channels()
#     H = nx.Graph()
#
#     for key, value in chnls.items():
#         for l in value:
#             H.add_edge(value[0].encode('utf-8'),l.encode('utf-8'), color='red')
#
#     # H.add_edge(2, 3, color='red')
#     # H.add_edge(1, 2, weight=4)
#     for u, v, data in H.edges_iter(data=True):
#         print u, v, data
#
#     plt.subplot(121)
#
#     nx.draw(H, with_labels=True, font_weight='bold')
#     plt.subplot(122)
#     nx.draw_shell(H, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
#
#     plt.show()


if __name__ == "__main__":

    # lst = classify_recipe_data()
    # get_most_popular_recipe(lst, 9)

    # lst = classify_channel_data()

    # lst = get_selected_channel_list()
    # lst1 = get_recipe_by_channel(lst)

    # print("printing x")
    # for l in lst1:
    #     print l

    # generate_interaction_chain()
    generate_interaction_chain_between_channels()

    # drawGraph()