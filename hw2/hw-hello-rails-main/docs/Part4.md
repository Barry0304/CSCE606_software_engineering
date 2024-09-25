# Part 4

## Change the database for production

<!---
In the Sinatra Wordguesser assignment, you already learned how to deploy a Sinatra app to Heroku. Deploying a Rails app is very similar, but a few extra steps are required since most Rails apps use databases.
--->

All apps on Heroku use the PostgreSQL database.  For Ruby/Rails apps to do so, they must include the `pg` gem.  However, we don't want to use this gem while developing, since we're using SQLite for that. Gemfiles let you specify that certain gems should only be used in certain environments.  Rails apps examine the environment variable `RAILS_ENV` to determine which environment they're running in, to make decisions such as which database to use (`config/database.yml`) and which gems to use. Heroku sets this variable to `production` at deploy time; running tests sets it to `test`; while you're running your app interactively, it's set to `development`. 

To specify production-specific gems, you must make **two** edits to your Gemfile.  First, add this: 

```
group :production do
  gem 'pg' # for Heroku deployment
end
```

(If there is already a `group :production` in your Gemfile, just add the `gem 'pg'` line to it.)

Second, find the line that specifies the `sqlite3` gem, and tell the Gemfile that that gem should **not** be used in production, by moving that line into its own group like so:

```
group :development, :test do
  gem 'sqlite3'
end
```

This second step is necessary because Heroku is set up in such a way that the `sqlite3` gem simply won't work, so we have to make sure it is _only_ loaded in development and test environments but _not_ production.

As always when you modify your Gemfile, re-run `bundle install` and commit the modified `Gemfile` and `Gemfile.lock`. If it errors out, run `bundle config set --local without 'production'` then run `bundle install`.  Also note that when you run Bundler, it will still compute dependencies and versions for gems in the `production` group, but it won't install them.  Heroku will use `Gemfile.lock` to install the matching versions of the gems when you deploy.

**Don't we have to modify `config/database.yml` as well?**  You'd think so, but the way Heroku works, it actually _ignores_ `database.yml` and forces Rails apps to use Postgres.  So modifying the `production:` section of `database.yml` won't have any effect on Heroku.

## Deploy to Heroku

The first time you use the Heroku command line tool, you will have to authenticate yourself using your Heroku username and password, by executing `heroku login`.  If you need to login from a terminal without a browser, you need to first login from a terminal on a machine with a browser, then run `heroku login` to authenticate yourself to Heroku, then run `heroku authorizations:create`, then copy the token value, then run `heroku login --interactive` on the browser-less terminal and use the token as your password.

At this point, having committed all changes locally, you should be ready to push your repository to Heroku for deployment.

Next, you need to create a new app "container" on Heroku to which you can deploy.  Since Heroku behaves like a Git repo that you push to, the app "container" must somehow be associated with your development repo.  The easiest way to do this is to use the  Heroku command line tool from within the app's root directory; execute `heroku help create` to see how. The created app container will then be associated with your app.  You can execute `git remote` to show a list of all remote Git repos associated with your app, among which `heroku` should now appear.  You can execute `git remote show heroku` to verify that pushing to the `heroku` "repo" will deploy to a URL on Heroku whose name matches the name you picked for your app.

Finally, you need to have a database provisioned for your application.  If you have not done so already, [install Heroku Postgres](https://elements.heroku.com/addons/heroku-postgresql), choose the Mini plan, and attach it to your app on Heroku.

OK, the moment of truth has arrived.  Execute `git push heroku main` to push the current head of your main branch to Heroku.  Heroku will try to install all the Gems in your gemfile and fire up your app!  You should be able to view your app at `https://your-app-name.herokuapp.com`! Right?

Nope. Heroku needs the `Procfile`.  Make a file named `Procfile` (no file extension) in the root of your app and put this line in it: `web: bundle exec rails server -p $PORT`.  Commit that change and push to Heroku again.  You should be able to view your app at `https://your-app-name.herokuapp.com`! Right?

Almost.  If you try this, you'll see a Heroku error.

<details>
<summary>
<b>Self-check question:</b> Use the command <code>heroku logs</code> to see the last several lines of error log messages from Heroku.  What caused the error?
</summary>
<blockquote>
As the error message <code>relation "movies" does not exist</code> tells us, there is no <code>movies</code> table on Heroku -- in fact there isn't even a  database.
</blockquote>
</details>

(It's worth making sure you understand the self-check question before charging on to the fix!)

## Fix Heroku deployment

Creating the database locally required 2 steps: first we ran the initial migration to create the `movies` table (schema), then we seeded the database with some initial data.  We must do these 2 steps on Heroku as well, by preceding each with `heroku run`, which just runs the corresponding command in a shell on Heroku:

```
heroku run rails db:migrate
```
Now go verify that you can visit your app, but no movies are listed...
```
heroku run rails db:seed
```
...and now your app should work on Heroku just as it does locally, with the seed data.

Note that in the future you should put these commands (migrate and seed) as worker processes in the `Procfile` to avoid manually typing them. This documentation may be helpful: [Release Phase](https://devcenter.heroku.com/articles/release-phase) and [Procfile](https://devcenter.heroku.com/articles/procfile#procfile-naming-and-location).

Voilà -- you have created and deployed your first Rails app!


<details>
<summary>
What are the two steps you must take to have your app use a particular Ruby gem? 
</summary>
<blockquote>
You must add a line to your <code>Gemfile</code> to add a gem and re-run <code>bundle install</code>.
</blockquote>
</details>

<details>
<summary>
The <i>first</i> time you deploy a particular app on Heroku, what steps do you need to take (assuming you have adjusted your <code>Gemfile</code> correctly as described above)?
</summary>
<blockquote>
Create the app container on Heroku; push the app to Heroku; run the initial migration(s) to create the database; and if appropriate, seed the database with initial data.
</blockquote>
</details>


<details>
<summary>
When you make changes to your app code, including adding new migrations, what must you do to <i>update</i> the existing Heroku app? (HINT: try making a simple change to the app, like changing something in a view, and see if you can deduce the sequence of steps.)
</summary>
<blockquote>
Commit changes to Git, then <code>git push heroku main</code> to redeploy. If you created new migrations, you also need to <code>heroku run rails db:migrate</code> to apply them on the Heroku side.
</blockquote>
</details>

## Next
[Part 5](Part5.md)
