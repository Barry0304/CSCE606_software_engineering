# Examples of Coverage Tools for Java, Python, and Ruby

[back to main page](README.md)

There are **many** tools which compute coverage for you for all of these lanugages.  Here, I will show you just one for each.  You are not required to use these tools (though, I do **highly** recommend them), but you must use some tool for computing coverage (because doing it by hand is too tedious).


## Java
Use [JaCoCo](https://www.jacoco.org/jacoco/). I think the easiest way is to use [the Maven plugin](https://www.jacoco.org/jacoco/trunk/doc/maven.html).

1. see [an example pom.xml](example_pom.xml) for how to include JaCoCo in your build.
2. run `mvn verify`
3. view the coverage report in `target/site/jacoco/index.html` in your browser
   + the raw data is in `target/site/jacoco/jacoco.csv`

## Python
Use [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/).

1. run `pytest --cov-report term --cov-report html --cov-report json --cov-branch --cov=app tests/`
   + use command line options and/or a configuration file to get more precise control as necessary/desired
2. view the coverage report
   + in the terminal
   + in `coverage.json`
   + in `htmlcov/index.html`

## Ruby
Use [SimpleCov](https://github.com/simplecov-ruby/simplecov).

1. Add SimpleCov to your `Gemfile`
   + `gem 'simplecov', group: :test`
2. run `bundle install`
3. load, configure, and launch SimpleCov at the very top of `spec/spec_helper.rb`
```ruby
require 'simplecov'
SimpleCov.start do
  add_filter "/spec/"
  enable_coverage :branch
  formatter SimpleCov::Formatter::HTMLFormatter
  minimum_coverage_by_file line: 90, branch: 90
end
```
4. run your tests: `rspec`
5. view the coverage report
   + in the terminal
   + in `coverage/index.html`
