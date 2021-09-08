# django-training
##Exercise

Create a CRUD API with Django and DRF that allows you to CRUD recipes and add/delete ingredients to it.  Test it using postman or similar.

Create automated tests for every action

Recipe: Name, Description
Ingredient: Name, Recipe (ForeignKey) ← assume a given ingredient belongs only to one recipe, even if that means multiple Ingredient instances with the exact same name.

## To run

Docker is used to run the Django app and the Django app and the PostgreSQL database containers:

To launch the containers locally:
> `docker-compose up`
 
To access the Django web interface locally, navigate to:
http://localhost:8000/api/recipe/

## Contributing

Tests and linting can be run with:
> `docker-compose run app sh -c "python manage.py test && flake8"`

## API

The following endpoints are implemented:
- GET /recipes
- GET /recipes/{recipe_id}
- GET /recipes/?name=SEARCHTEXT
- POST /recipes
- PATCH /recipes/{recipe_id}
- DELETE /recipes/{recipe_id}

## Canonical data model
Recipes and ingredients are encapsulated within a single model at the API level as follows:
```json
{
  "name": "recipe name",
  "description": "recipe description",
  "ingredients": [
    { "name": "flour" },
    { "name": "butter" },
    { "name": "sugar" }
  ]
}
```
This is expressed in two models at the ORM level, with ingredient having a foreign key to reference the recipe.
