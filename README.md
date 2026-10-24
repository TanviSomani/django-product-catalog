# Django Product Catalog

A small Django app for browsing sample products. The main page searches product descriptions and filters by category and tag. Search and filters can be combined.

## Try it online with Replit

1. Download this project ZIP and extract it on your computer.
2. Sign in to Replit and create a new Python project.
3. Upload the project files and folders into the Replit project, keeping the folder structure.
4. Replit should detect `requirements.txt` and install Django. If it does not, open the Shell and run `pip install -r requirements.txt`.
5. Click **Run**. The `.replit` run command applies migrations, creates sample data, and starts Django on port 3000.
6. Open the web preview to try searching and filtering products.

If Replit asks you to select a run command, use:

```bash
python manage.py migrate && python manage.py seed_data && python manage.py runserver 0.0.0.0:3000
```

The seed command is safe to run again. It creates the example records if they are missing and updates the product tags.

## Run locally (optional)

You need Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Then run:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the catalog and http://127.0.0.1:8000/admin/ for the admin interface.

To create an admin login, run `python manage.py createsuperuser`.

## Sample data

The `seed_data` command creates 5 categories, 10 tags, and 20 example products. The assignment asks for sample data to be entered using Django admin; these records are provided to make the project quick to test. You can also add or edit records in the admin interface.

## Search and filter behavior

- Search checks product descriptions using a case-insensitive partial match.
- Category selects products in that category.
- Tag selects products associated with that tag.
- Active conditions are combined, so a product must match the description search (if entered), the selected category (if selected), and the selected tag (if selected).
- The page shows a message when no products match.

## Tests

Run:

```bash
python manage.py test
```

The tests cover description search, category filtering, tag filtering, combined filters, and the no-results case.

## Notes

- `Product.category` is a foreign key. Categories with products cannot be deleted because the relationship uses `PROTECT`.
- `Product.tags` is many-to-many: a product can have several tags and each tag can be used by several products.
- `select_related()` and `prefetch_related()` reduce extra database queries while rendering products.
- SQLite is used so no separate database service is required.
- `ALLOWED_HOSTS` is open for easy use in a temporary online demo. Restrict it before deploying a public production site.
