
import os
import pandas as pd
from plotly import graph_objs as go
import matplotlib.pyplot as plt

from . segments import Segments

def plotly_go(segments):
    sl = segments['left']
    sr = segments['right']

    data = []
    for seg1 in sr._segments:
        tmp = go.Scatter( x=[seg1._x0, seg1._x1], 
                          y=[seg1._y0, seg1._y1],
                          mode = 'lines',
                          showlegend=False,
                          line = dict(
                                width = 3,
                                color = 'rgba(207, 0, 15, 0.65)',
                          )
                        )
        data.append(tmp)

    for seg1 in sl._segments:
        tmp = go.Scatter( x=[seg1._x0, seg1._x1], 
                          y=[seg1._y0, seg1._y1],
                          mode = 'lines',
                          showlegend=False,
                          line = dict(
                                width = 2,
                                dash = 'dot',
                                color = 'rgba(51, 110, 123, 0.65)',
                            )
                        )
        data.append(tmp)
    
    return data

def plotly_layout(title=""):
    lay = go.Layout(showlegend=False,
                       title=title,
                       hovermode="closest",
                       yaxis=dict(title="time", 
                                  autorange='reversed',
                                  zeroline=False,
                                  showline=False),
                       xaxis=dict(title="distance(km)",
                                  zeroline=False,
                                  showline=False),
                       )
    return lay

def matplotlib_plot(segments):

    sl = segments['left']
    sr = segments['right']

    fig, ax = plt.subplots(figsize=(12,6))

    # plt.axvline(xf, color='lightgrey', linestyle="--")
    # plt.axvline(x0, color='lightgrey', linestyle="--")
    # plt.axvline(x1, color='lightgrey', linestyle="--")
    # plt.plot( [x0, x1], [y0, y0], color="lightgrey")
    # plt.plot( xf, y0, 'o', color='red')

    for seg1 in sl._segments:
        tmp = go.Scatter( x=[seg1._x0, seg1._x1], 
                          y=[seg1._y0, seg1._y1],
                          mode = 'lines',
                          showlegend=False,
                          line = dict(
                                width = 2,
                                dash = 'dot',
                                color = 'rgba(51, 110, 123, 0.65)',
                            )
                        )
       
    # for seg1, seg2 in zip(sl._segments, sr._segments):
    #     if seg1._y0 < ymax:
    #         plt.plot( [seg1._x0, seg1._x1], [seg1._y0, seg1._y1], lw=1, color="red", alpha=(sr._depth-seg1._depth)/sr._depth)

    #     if seg2._y0 < ymax:
    #         plt.plot( [seg2._x0, seg2._x1], [seg2._y0, seg2._y1], lw=1, color="blue", alpha=(sr._depth-seg1._depth)/sr._depth)
    
    # plt.ylim(0, ymax)
    ax.invert_yaxis()
    return ax


def plot_one_many(config, df, s):
    fig = plt.figure(figsize=(14,8))
    
    ax = []
    gs = fig.add_gridspec(1,7)
    ax.append(fig.add_subplot(gs[0]))
    ax.append(fig.add_subplot(gs[1], sharey=ax[0]))
    ax.append(fig.add_subplot(gs[2:5], sharey=ax[0]))
    ax.append(fig.add_subplot(gs[5], sharey=ax[0]))
    ax.append(fig.add_subplot(gs[6], sharey=ax[0]))

    for a in ax[1:]:
        plt.setp(a.get_yticklabels(), visible=False)

    ax[0].plot(df['I_BS2'].values, df.index)
    ax[0].set_ylim(s.range())
    ax[0].set_title("I_BS2")
    
    ax[1].plot(df['I_BS1'].values, df.index)
    ax[1].set_ylim(s.range())
    ax[1].set_title("I_BS1")

    s.plot(ax=ax[2], lw=2)

    ax[3].plot(df['I_BN1'].values, df.index)
    ax[3].set_ylim(s.range())
    ax[3].set_title("I_BN1")

    ax[4].plot(df['I_BN2'].values, df.index)
    ax[4].set_ylim(s.range())
    ax[4].set_title("I_BN2")
    
    # critical points...
    for a in ax:
        for x in s._segments:
            a.axhline(x._y1, linestyle="--", lw=1, color='black', alpha=0.25)

    title = "{}\n{}, {}, {}".format(os.path.basename(config.get('filename')), 
                                        config.get('loss'), 
                                        config.get('shape'), 
                                        config.get('imp'))
    
    filename = os.path.basename(config.get('filename')).replace(".txt", '.png')
    #fig.suptitle(title, fontsize=14)
    ax[2].set_title(title)
    ax[2].set_xlabel("Distance (km)")
    
    ax[0].set_ylabel("Time (s)")
    plt.savefig(filename)




def plot_one(config, df, s):
    
    fig, ax = plt.subplots(1, 3, figsize=(14,8), sharey=True)
    
    for a in ax[1:]:
        plt.setp(a.get_yticklabels(), visible=False)
    
    ax[0].plot(df['I_BS1'].values, df.index, label="I_BS1")
    ax[0].plot(df['I_BS2'].values, df.index, label="I_BS2")
#     ax[0].plot(df['I_BS3'].values, df.index, label="I_BS3")
#     ax[0].plot(df['I_BS4'].values, df.index, label="I_BS4")
#     ax[0].plot(df['I_BS5'].values, df.index, label="I_BS5")
#     ax[0].plot(df['I_BS6'].values, df.index, label="I_BS6")
#     ax[0].plot(df['I_BS7'].values, df.index, label="I_BS7")
    
    ax[0].set_ylim(s.range())
    ax[0].legend()
    
    s.plot(ax=ax[1], lw=2)

    ax[2].plot(df['I_BN1'].values, df.index, label="I_BN1")
    ax[2].plot(df['I_BN2'].values, df.index, label="I_BN2")
#     ax[2].plot(df['I_BN3'].values, df.index, label="I_BN3")
#     ax[2].plot(df['I_BN4'].values, df.index, label="I_BN4")
#     ax[2].plot(df['I_BN5'].values, df.index, label="I_BN5")
#     ax[2].plot(df['I_BN6'].values, df.index, label="I_BN6")
#     ax[2].plot(df['I_BN7'].values, df.index, label="I_BN7")
    ax[2].set_ylim(s.range())
    ax[2].legend()

    # critical points...
    for a in ax:
        for x in s._segments:
            a.axhline(x._y1, linestyle="--", lw=1, color='black', alpha=0.25)

    title = "{}\n{}, {}, {}".format(os.path.basename(config.get('filename')), 
                                        config.get('loss'), 
                                        config.get('shape'), 
                                        config.get('imp'))
    
    filename = os.path.basename(config.get('filename')).replace(".txt", '.png')
    #fig.suptitle(title, fontsize=14)
    ax[1].set_title(title)
    ax[1].set_xlabel("Distance (km)")
    
    ax[0].set_ylabel("Time (s)")
    plt.tight_layout()
    plt.savefig(filename)
    
        
def plot_seven(config, df, s):
    
    fig, ax = plt.subplots(1, 3, figsize=(14,8), sharey=True)
    
    for a in ax[1:]:
        plt.setp(a.get_yticklabels(), visible=False)
    
    ax[0].plot(df['I_BS1'].values, df.index, label="I_BS1")
    ax[0].plot(df['I_BS2'].values, df.index, label="I_BS2")
    ax[0].plot(df['I_BS3'].values, df.index, label="I_BS3")
    ax[0].plot(df['I_BS4'].values, df.index, label="I_BS4")
    ax[0].plot(df['I_BS5'].values, df.index, label="I_BS5")
    ax[0].plot(df['I_BS6'].values, df.index, label="I_BS6")
    ax[0].plot(df['I_BS7'].values, df.index, label="I_BS7")
    
    ax[0].set_ylim(s.range())
    ax[0].legend()
    
    s.plot(ax=ax[1], lw=2)

    ax[2].plot(df['I_BN1'].values, df.index, label="I_BN1")
    ax[2].plot(df['I_BN2'].values, df.index, label="I_BN2")
    ax[2].plot(df['I_BN3'].values, df.index, label="I_BN3")
    ax[2].plot(df['I_BN4'].values, df.index, label="I_BN4")
    ax[2].plot(df['I_BN5'].values, df.index, label="I_BN5")
    ax[2].plot(df['I_BN6'].values, df.index, label="I_BN6")
    ax[2].plot(df['I_BN7'].values, df.index, label="I_BN7")
    ax[2].set_ylim(s.range())
    ax[2].legend()

    # critical points...
    for a in ax:
        for x in s._segments:
            a.axhline(x._y1, linestyle="--", lw=1, color='black', alpha=0.25)

    title = "{}\n{}, {}, {}".format(os.path.basename(config.get('filename')), 
                                        config.get('loss'), 
                                        config.get('shape'), 
                                        config.get('imp'))
    
    filename = os.path.basename(config.get('filename')).replace(".txt", '.png')
    #fig.suptitle(title, fontsize=14)
    ax[1].set_title(title)
    ax[1].set_xlabel("Distance (km)")
    
    ax[0].set_ylabel("Time (s)")
    plt.tight_layout()
    plt.savefig(filename)

def plot_config(config):
    
    # check the configuration
    assert config.get('lines') in ['one', 'seven']
    assert config.get('loss') in ['lossless', 'lossy']
    assert config.get('shape') in ['impulse', 'square']
    assert config.get('imp') in ['fault', 'no fault']
    
    if config.get('lines') == 'one':
        
        if config.get('loss') == 'lossless':
            config['speed'] = {'l1': 299800}
            
        if config.get('loss') == 'lossy':
            config['speed'] = {'l1': 236090}
            
        config['length'] = {'l1': 1 }
        config['fault_location'] =  {'l1': 0.25 }
        
        assert len(config.get('speed').values()) == 1
        assert len(config.get('length').values()) == 1
        
    if config.get('lines') == 'seven':
        
        if config.get('loss') == 'lossless':
            
            config['speed'] = {'l1': 299800,
                               'l2': 299800,
                               'l3': 299800,
                               'l4': 299800,
                               'l5': 299800,
                              }
            
        if config.get('loss') == 'lossy':
            config['speed'] = {'l1': 236090,
                               'l2': 217860,
                               'l3': 236090,
                               'l4': 217860,
                               'l5': 236090
                              }

        config['length'] = {'l1': 0.7,
                            'l2': 0.6,
                            'l3': 1,
                            'l4': 0.5,
                            'l5': 0.7,
                           }
        
        config['fault_location'] =  {'l3': 0.25 }
        
        assert len(config.get('speed').values()) == 5
        assert len(config.get('length').values()) == 5

    assert len(config.get('fault_location')) == 1
    
    # read timeseries data
    df = pd.read_csv(config.get('filename'))
    df.set_index("X axis", inplace=True)
    
#     print(df.columns)
    
#     if config.get('lines') == 'one':
#         assert len(df.columns) == 8
    
#     if config.get('lines') == 'seven':
#         assert len(df.columns) == 25
    
    # create lattice
    if config.get('lines') == 'seven':
        
        dist = [-1*(config.get('length').get('l1')+config.get('length').get('l2')),
                -1*config.get('length').get('l2'),
               0, 
               config.get('fault_location').get('l3'), 
               config.get('length').get('l3'),
               config.get('length').get('l3') + config.get('length').get('l4'),
               config.get('length').get('l3') + config.get('length').get('l4') + config.get('length').get('l5'),
              ]
        
        speed = [ config.get('speed').get('l1'), 
                  config.get('speed').get('l2'),
                  config.get('speed').get('l3'),
                  config.get('speed').get('l3'),
                  config.get('speed').get('l4'),
                  config.get('speed').get('l5')]
        
        lattice = Segments(dist, speed, 3)
        
        lattice.create(lines=config.get('depth'))
        plot_seven(config, df, lattice)
   
    if config.get('lines') == 'one':
        
        
        lattice = Segments([0, 
                        config.get('fault_location').get('l1'), 
                        config.get('length').get('l1')], 
                        [config.get('speed').get('l1'), 
                        config.get('speed').get('l1')], 
                        1)
        
        lattice.create(lines=config.get('depth'))
        plot_one(config, df, lattice)