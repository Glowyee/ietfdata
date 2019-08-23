from ietfdata.datatracker import *
import plotly.figure_factory as ff
import plotly.io as pio
import dateutil.parser

data = DataTracker()  # assigning the imported module(datatracker to a local variable)


def main_doc_name():
    """
    Information about a document in the datatracker

    Parameters:
        none

    Returns:
        the name of the document
    """
    doc = data.document_from_draft("draft-ietf-bess-evpn-proxy-arp-nd")
    doc_name = doc.name

    return doc_name


def main_doc_versions():
    """
    Lookup information about a document in the datatracker,
    gets all submissions, lookup individual submission object using
    submission function in the datatracker and
    gets the version number.

    Parameters:
        none

    Returns:
        all version number of the document
    """
    versions = []

    doc = data.document_from_draft("draft-ietf-bess-evpn-proxy-arp-nd")
    doc_submissions = doc.submissions

    for submission in range(len(doc_submissions)):
        for j in data.submission(doc_submissions[submission]):
            versions.append(j.rev)

    return versions


def main_version_dates():
    """
    Lookup information about a document in the datatracker,
    gets all submissions, lookup individual submission object using
    submission function in the datatracker and
    gets the version dates.

    Parameters:
        none

    Returns:
        all versions created date
    """
    created_date = []
    doc = data.document_from_draft("draft-ietf-bess-evpn-proxy-arp-nd")
    doc_submissions = doc.submissions

    doc_expires = doc.expires

    date = dateutil.parser.parse(doc_expires).date()
    y = date.strftime('%Y-%m-%d')

    for submission in range(len(doc_submissions)):
        for j in data.submission(doc_submissions[submission]):
            created_date.append(j.submission_date)

    created_date.append(y)
    created_date.sort()

    return created_date


def doc_replacement():
    """
    Lookup a document's history in the datatracker,
    gets the document's id and lookup the document it replaced
    using the related_document_history function and
    gets name of the document replaced.

    Parameters:
        none

    Returns:
        name of the document replaced
    """
    doc_history = []

    for history in data.document_history("draft-ietf-bess-evpn-proxy-arp-nd"):
        doc_history.append(history)

    replacement_id = doc_history[-1].id

    for doc in data.related_document_history(str(replacement_id), "replaces"):
        replaced = doc.target

    splits = replaced.split("/")
    doc_name = splits[5]

    return doc_name


replaced_doc = doc_replacement()  # assigns the replaced document to a local variable to be used by another function.


def doc_replaced_versions():
    """
    Lookup information about the replaced document in the datatracker,
    gets all submissions, lookup individual submission object using
    submission function in the datatracker and
    gets the version number.

    Parameters:
        none

    Returns:
        all versions number of the replaced document
    """
    versions = []

    doc = data.document_from_draft(replaced_doc)
    doc_submissions = doc.submissions

    for submission in range(len(doc_submissions)):
        for j in data.submission(doc_submissions[submission]):
            versions.append(j.rev)

    return versions


def doc_replaced_dates():
    """
    Lookup information about the replaced document in the datatracker,
    gets all submissions, lookup individual submission object using
    submission function in the datatracker and
    gets the version dates of the replaced document.

    Parameters:
        none

    Returns:
        all versions created date for the replaced document
    """
    created_date = []

    doc = data.document_from_draft(replaced_doc)
    doc_submissions = doc.submissions

    doc_expires = doc.expires

    date = dateutil.parser.parse(doc_expires).date()
    d = date.strftime('%Y-%m-%d')

    for submission in range(len(doc_submissions)):
        for j in data.submission(doc_submissions[submission]):
            created_date.append(j.submission_date)

    created_date.append(d)
    created_date.sort()

    return created_date


# =================== assigning all returned result to a local variable =========================
main_doc = main_doc_name()

main_version = main_doc_versions()
main_version.sort()

main_dates = main_version_dates()

replaced_name = doc_replacement()

replaced_versions = doc_replaced_versions()
replaced_versions.sort()

replacement_dates = doc_replaced_dates()


def document_visualization():
    """
    Uses all the data retrieved for a document
    and its replacement to create a chart that
    shows the different versions of both document
    and their created dates

    Parameters:
        none

    Returns:
        a figure representing the data retrieved
    """
    df = []

    for i in range(len(replacement_dates) - 1):
        list_ = dict(Task=replaced_doc, Start=replacement_dates[i], Finish=replacement_dates[i + 1],
                     Resource=replaced_versions[i])
        df.append(list_)

    for i in range(len(main_dates) - 1):
        list_ = dict(Task=main_doc, Start=main_dates[i], Finish=main_dates[i + 1], Resource=main_version[i])
        df.append(list_)

    fig = ff.create_gantt(df, group_tasks=True, index_col='Resource',
                          title='An example of a document, its versions and document it replaced',
                          show_colorbar=True,
                          showgrid_x=True,
                          showgrid_y=True)

    fig['layout'].update(autosize=False, width=1000, height=600, margin=dict(l=300, pad=10))

    fig.show()


document_visualization()  # calls the visualisation
