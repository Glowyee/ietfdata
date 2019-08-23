from ietfdata.datatracker import *
import plotly.figure_factory as ff
import plotly.io as pio
import dateutil.parser
import random

data = DataTracker()  # assigning the imported module(datatracker to a local variable)


def get_active_wg_area(area_id):
    """
        Get the names of all active working groups in a particular area
        IDs for the area needs to be known to use this function.

        IETF AREAS (ACRONYMS)                                            ID
        Routing(rtg)                                                     1249
        Internet(int)                                                    1052
        Application and real-time(art)                                   2010
        General(gen)                                                     1008
        Operations & Management(ops)                                     1193
        Security(sec)                                                    1260
        Transport(tsv)                                                   1324

        :parameter:
            takes in the area id

        :returns:
            the names of the group under an area with that specified id
    """
    area_list = []
    for active_area in data.active_wg_area(area_id):
        area_list.append(active_area.name)

    area_list.sort()
    return area_list


def get_document(group_id):
    """
    Lookup documents under a particular group, gets the name,
    expiring date and date of creation

    :param group_id:
        Takes in the group id

    :return:
        the name of the document, when it was created and when it expires
    """
    doc_name = []
    doc_expires = []
    expires = []
    doc_submissions = []
    submit_date = []
    doc_result = []

    for doc in data.area_group_document(group_id, "draft", "1"):
        doc_name.append(doc.title)
        doc_expires.append(doc.expires)
        doc_submissions.append(doc.submissions[0])

    for d in range(len(doc_expires)):
        result = dateutil.parser.parse(doc_expires[d]).date()
        y = result.strftime('%Y-%m-%d')
        expires.append(y)

    for submission in range(len(doc_submissions)):
        for j in data.submission(doc_submissions[submission]):
            submit_date.append(j.submission_date)

    for i in range(len(doc_name)):
        temp = [doc_name[i], expires[i], submit_date[i]]
        doc_result.append(temp)

    return doc_result


# ============ documents returned under a specific group is assigned to a local variable ======================= #
# ============ The routing area (1249) has the following group active groups with their ids ===== #
group = get_active_wg_area("1249")

bes = get_document("1960")

bier = get_document("1964")

bfd = get_document("1628")

brp = get_document("2150")

ccmp = get_document("1524")

dnet = get_document("1962")

idr = get_document("1041")

irs = get_document("1875")

lisp = get_document("1751")

man = get_document("1132")

mls = get_document("1140")

nvo = get_document("1840")

pce = get_document("1630")

pim = get_document("1397")

pls = get_document("1969")

rawg = get_document("1619")

rpn = get_document("1730")

sfd = get_document("1910")

sprn = get_document("1905")

teas = get_document("1985")

# all document under each group is placed in the list groups

groups = [bes, bier, bfd, brp, ccmp, dnet, idr, irs, lisp, man,
          mls, nvo, pce, pim, pls, rawg, rpn, sfd, sprn, teas]


def visualization():
    """
    Uses all the retrieved for documents
    under a specific active working group in an area
    to create a chart that
    shows the life span of the document.

    Parameters:
        none

    Returns:
        a figure representing the data retrieved
    """
    r = lambda: random.randint(0, 255)  # gets random color for all documents in a specific group
    colors = ['#%02X%02X%02X' % (r(), r(), r())]

    df = []

    for i in range(len(groups)):
        for doc, start, end in groups[i]:
            list_ = dict(Task=doc, Start=start, Finish=end, Resource=group[i])
            df.append(list_)
            colors.append('#%02X%02X%02X' % (r(), r(), r()))

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', title='Document Life Span',
                          show_colorbar=True,
                          showgrid_x=True,
                          showgrid_y=True)
    fig['layout'].update(autosize=False, width=1200, height=3000, margin=dict(l=300, pad=10))
    fig.show()


visualization()  # calls the visualization
