import os

def read_file(filename):
    """Reads a file and returns a list of non-empty lines."""
    if os.path.exists(filename):
        with open(filename, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

logins = read_file("login_list.txt")
issues = read_file("link_list.txt")
packs = read_file("pack_list.txt")

nation_issues = {}
nation_packs = {}

def group_links_by_nation(links, storage_dict):
    """Groups links by nation name."""
    for link in links:
        if "nation=" in link:
            nation_name = link.split("nation=")[1].split("/")[0]
            storage_dict.setdefault(nation_name, []).append(link)

group_links_by_nation(issues, nation_issues)
group_links_by_nation(packs, nation_packs)

html_filename = "gotMajorIssues.html"
with open(html_filename, "w", encoding="utf-8") as links:
    links.write("""\
<html>
<head>
<style>
    td.createcol p { padding-left: 10em; }
    a { text-decoration: none; color: black; }
    a:visited { color: grey; }
    table { border-collapse: collapse; border: 1px solid darkorange; width: 100%; }
    tr, td { border-bottom: 1px solid darkorange; padding: 0.5em; }
    tr:hover { background-color: lightgrey; cursor: pointer; }
</style>
</head>
<body>
<table>
""")

    processed_nations = set()

    for login in logins:
        if "nation=" not in login:
            continue

        nation_name = login.split("nation=")[1].split("&")[0]

        if nation_name in processed_nations:
            continue  # Skip nations without issues or packs
        
        processed_nations.add(nation_name)

        # Login row
        login_url = f"{login}"
        links.write(f"""<tr><td colspan="3"><p><a target="_blank" href="{login_url}">Log in to Nation {nation_name}</a></p></td></tr>\n""")

        # Issue links
        for issue in nation_issues.get(nation_name, []):
            links.write(f"""<tr><td><p><a target="_blank" href="{issue}">Link to Issue</a></p></td></tr>\n""")

        # Pack links
        for pack in nation_packs.get(nation_name, []):
            links.write(f"""<tr><td><p><a target="_blank" href="{pack}">Link to Pack</a></p></td></tr>\n""")

    # JavaScript for auto-removing rows on click
    links.write("""\
</table>
<script>
document.querySelectorAll("tr").forEach(row => {
    row.addEventListener("click", function() {
        let nextRow = row.nextElementSibling;
        row.remove();
        if (nextRow) {
            let nextLink = nextRow.querySelector("a");
            if (nextLink) {
                nextLink.focus();
            }
        }
    });
});
</script>
</body>
</html>
""")

print(f"HTML file '{html_filename}' created successfully.")