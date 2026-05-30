from django.shortcuts import render, redirect
from . import util
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):

    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found."
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })


def search(request):

    query = request.GET.get("q", "")

    entries = util.list_entries()

    for entry in entries:
        if entry.lower() == query.lower():
            return redirect("entry", title=entry)

    results = [
        entry for entry in entries
        if query.lower() in entry.lower()
    ]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })


def new_page(request):

    if request.method == "POST":

        title = request.POST["title"]
        content = request.POST["content"]

        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists."
            })

        util.save_entry(title, content)

        return redirect("entry", title=title)

    return render(request, "encyclopedia/new_page.html")


def edit_page(request, title):

    if request.method == "POST":

        content = request.POST["content"]

        util.save_entry(title, content)

        return redirect("entry", title=title)

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": util.get_entry(title)
    })


def random_page(request):

    title = random.choice(util.list_entries())

    return redirect("entry", title=title)