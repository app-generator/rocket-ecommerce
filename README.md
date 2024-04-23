<div align="center">
    <a href="https://appseed.us/product/rocket-ecommerce/django/">
        <img src="https://github-production-user-asset-6210df.s3.amazonaws.com/51070104/272178364-cbac6d97-b2dc-4d95-bab6-891f4ee7d84d.png"" width="64" height="64" alt="Rocket Icon">
    </a>
    <h1>
        <a href="https://appseed.us/product/rocket-ecommerce/django/">
            Rocket eCommerce
        </a>
    </h1>
    <p>
        <strong>Django</strong> &bull; <strong>TailwindCSS</strong> &bull; <strong>Stripe</strong> &bull; <strong>Analytics</strong> &bull; <strong>Docker</strong> &bull; <strong>CI/CD</strong> &bull; <strong>Lifetime Updates</strong> &bull; <strong>Unlimited Projects</strong>
    </p>  
    <h3>     
        <a target="_blank" href="https://rocket-ecommerce.onrender.com">
            Demo
        </a>
        &nbsp; &bull; &nbsp;
        <a target="_blank" href="https://appseed.us/support/">
           Support
        </a>
        &nbsp; &bull; &nbsp;
        <a target="_blank" href="https://appseed.us/product/rocket-ecommerce/django/#pricing">
           Buy License
        </a>
    </h3>    
    <p>
        <strong>Once authenticated, the ADMIN (superuser) can import the products from Stripe and customize each one locally by adding properties like Images, Tags, Discount, .. etc.</strong>
        <br /> <br />
        The product comes with <strong>Docker</strong> and <a href="https://deploypro.dev/" target="_blank">CI/CD Support</a>
    </p>  
    <hr />
</div>

<br />

<div align="center">
    <img src="https://github.com/app-generator/rocket-ecommerce/assets/51070104/1f4b1fa1-321a-4824-aeae-62021e9b7d17" alt="Rocket eCommerce - Django Starter styled with Tailwind and Flowbite.">
</div>

<br />

## Why [Rocket eCommerce](https://appseed.us/product/rocket-ecommerce/django/) 

> Affordable, actively supported eComemrce solution that requires minimal configuration - **[Buy License](https://appseed.us/product/rocket-ecommerce/django/#pricing)**

<br />

#### 👉 ***Supercharge your eCommerce App instantly, launch faster, make $***

Login users, process payments and send emails at lightspeed. Spend your time building your startup, not integrating APIs. 
**Rocket eCommerce** provides you with the boilerplate code you need to launch, FAST. 

#### 👉 ***Rocket your startup in days, not weeks*** 

The Django boilerplate has all you need to build your SaaS, Analytics tool, or any other type of Web App. From idea to production in 5 minutes.

#### 👉 **48+ hours of headaches**

 - 1 hrs to set up the project 
 - 2 hrs integrate tooling
 - 2 hrs to handle Stripe
 - 1 hrs for Docker
 - ∞ hrs overthinking...
 - Free [Support](https://appseed.us/support/) via `Email` & [Discord](https://discord.gg/fZC6hup) 

<br />

## Features 

| Status | Item | info | 
| --- | --- | --- |
| ✅ | Stack | Django, Tailwind, React |
| ✅ | Payments | Stripe |
| ✅ | Categories | YES |
| ✅ | Tags | YES |
| ✅ | Checkout | YES |
| ✅ | Discounts Page | YES |
| ✅ | Products Import | Stripe |
| ✅ | Products Local Customization | YES |
| ✅ | Analitycs | Weekly, Monthly, Year `Sales` |
| ✅ | Transactions Tracking | YES |
| ✅ | Docker | YES |
| ✅ | CI/CD | Render |
| ✅  | Active versioning and [support](https://appseed.us/support/) | [AppSeed](https://appseed.us/) |
| ✅  | [AWS, DO, Azure Deploy Assistance](https://deploypro.dev/)   | `DeployPRO` |

<br />

## Manual Build 

> 👉 Download code (public access)

```bash
$ git clone https://github.com/app-generator/rocket-ecommerce.git
$ cd rocket-ecommerce
```

> 👉 Create `.env` from `env.sample`

The most important, are the `Stripe Keys` **STRIPE_SECRET_KEY**, **STRIPE_PUBLISHABLE_KEY** that will connect your `Stripe` account with the APP.

```env
DEBUG=True

SECRET_KEY=<STRONG_KEY_HERE>

DEMO_MODE=True

STRIPE_SECRET_KEY=<YOUR_KEY_HERE>
STRIPE_PUBLISHABLE_KEY=<YOUR_KEY_HERE>

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

> 👉 Install **Django** modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

> 👉 Install **Tailwind/Flowbite** (separate terminal)

```bash
$ npm install
$ npm run dev        
```

> 👉 Migrate DB

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

> 👉 Seed DB

```bash
$ python manage.py seed_tags
```

> 👉 `Create Superuser` & Start the APP

```bash
$ python manage.py createsuperuser # create the admin
$ python manage.py runserver       # start the project
```

<br />

## Start With Docker

> 👉 Download code (public access)

```bash
$ git clone https://github.com/app-generator/rocket-ecommerce.git
$ cd rocket-ecommerce
```

> 👉 Start with Docker Compose

```bash
$ docker-compose up --build 
``` 

Visit the app in the browser `localhost:5085`.

<br />

## Use `MySql`

By default, the starter uses SQLite for persistence. In order to use MySql, here are the steps: 

- Start the MySql Server
- Create a new DataBase
- Create a new user with full privileges over the database 
- Install the MySql Python Driver (used by Django to connect)
  - `$ pip install mysqlclient`
- Edit the `.env` with the SQL Driver Information & DB Credentials 

```env

DB_ENGINE=mysql
DB_HOST=localhost
DB_NAME=<DB_NAME_HERE>
DB_USERNAME=<DB_USER_HERE>
DB_PASS=<DB_PASS_HERE>
DB_PORT=3306

```

Once the above settings are done, run the migration & create tables: 

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

## Production Build

> For issues, contact [support](https://appseed.us/support/) (eMail & Discord)

To use the starter in production mode, here are the steps: 

- Set  **DEBUG=False** in `.env`
- Execute `collectstatic` command
  - `$ python manage.py collectstatic --no-input`

As a model, feel free to take a look at [build.sh](./build.sh), the file executed by the CI/CD flow for Render.

<br />

## **Deploy on [Render](https://render.com/)**

- Create a Blueprint instance
  - Go to https://dashboard.render.com/blueprints this link.
- Click `New Blueprint Instance` button.
- Connect the `repo` that you want to deploy.
- Fill the `Service Group Name` and click on the `Update Existing Resources` button.
- Edit the Environment and [specify the PYTHON_VERSION](https://render.com/docs/python-version)
  - Version `3.11.5` was used for **[this deployment](https://rocket-django.onrender.com/)**
- After that, your deployment will start automatically.

At this point, the product should be LIVE.

<br />

## Codebase 

```bash
< PROJECT ROOT >
   |
   |-- core/                 # Project Settings 
   |    |-- settings.py 
   |    |-- wsgi.py     
   |    |-- urls.py     
   |
   |-- home/                 # Presentation app 
   |    |-- views.py         # serve the HOMEpage  
   |    |-- urls.py     
   |    |-- models.py
   |
   |-- apps/                 # Utility Apps 
   |    |-- common/          # defines models & helpers
   |    |    |-- models.py   
   |    |    |-- util.py 
   |    |-- users            # Handles Authentication 
   |    |-- api              # DRF managed API
   |    |-- charts           # Showcase Different Charts
   |    |-- tables           # Implements DataTables
   |    |-- tasks            # Celery, async processing
   |
   |-- templates/            # UI templates 
   |-- static/               # Tailwind/Flowbite 
   |    |-- src/             # 
   |         |-- input.css   # CSS Styling
   |
   |-- Dockerfile            # Docker
   |-- docker-compose.yml    # Docker 
   |
   |-- render.yml            # CI/CD for Render
   |-- build.sh              # CI/CD for Render 
   |
   |-- manage.py             # Django Entry-Point
   |-- requirements.txt      # dependencies
   |-- .env                  # ENV File
   |
   |-- *************************************************      
```   

<br />

## License

[EULA License](https://github.com/app-generator/license-eula)

<br />

---
[Rocket eCommerce](https://appseed.us/product/rocket-ecommerce/django/) - `eCommerce Starter` powered by **Django** and `Tailwind/Flowbite`.
