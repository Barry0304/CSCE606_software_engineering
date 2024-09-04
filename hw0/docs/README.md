# StatusBoard: Tell everyone your name and status.

Your task is to write a [REST](https://en.wikipedia.org/wiki/REST)ful-ish terminal application that lets people share and update their name and status.

Here are a couple examples of how this App should look and behave (there are many more [interaction examples](#interaction-examples) below):

```text
$ ./app
Welcome to the App!

login: ./app 'login <username> <password>'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
people: ./app 'people'
```

```text
$ ./app 'people'
People
------
Bob @bob (./app 'show bob')
  talking to alice
  @ 2024-07-18 21:14:57
Eve @eve (./app 'show eve')
  listening to alice and bob
  @ 2024-07-18 21:14:56
Dave @dave (./app 'show dave')
  zzz
  @ 2024-07-18 21:14:55
Alice @alice (./app 'show alice')
  listening to bob
  @ 2024-07-18 21:14:54

find: ./app 'find <pattern>'
sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
home: ./app
```

## REST

**REST** (**RE**presentational **S**tate **T**ransfer) is a software architectural style that was created to guide the design and development of the architecture for the World Wide Web.

The REST architectural style defines 5+1 guiding constraints which, when applied to system architecture, support desirable non-functional properties such as performance, scalability, simplicity, modifiability, visibility, portability, and reliability:

1. **Client/Server** - Client are separated from servers by a well-defined interface
2. **Stateless** - A specific client does not consume server storage when it is "at rest"
3. **Cache** - Responses indicate their own cacheability
4. **Uniform Interface**
   - Resource Identification in Requests - Individual resources are identified in requests using URIs.
   - Resource Manipulation Through Representations - When a client holds a representation of a resource, including any metadata attached, it has enough information to modify or delete the resource's state.
   - Self-descriptive Messages - Each message includes enough information to describe how to process the message.
   - Hypermedia As The Engine Of Application State - Having accessed an initial URI for the REST application—analogous to a human Web user accessing the home page of a website—a REST client should then be able to use server-provided links dynamically to discover all the available resources it needs.
5. **Layered System** - A client cannot ordinarily tell whether it is connected directly to the end server, or to an intermediary along the way
6. **Code on Demand** (*optional*) - Servers are able to temporarily extend or customize the functionality of a client by transferring logic to the client that can be executed within a standard virtual machine

Source: [REST - Wikipedia](https://en.wikipedia.org/wiki/REST)

For this assignment, we will make use of principles 1 (Client/Server), 2 (Stateless), 4 (Uniform Interface), and 5 (Layered System).

* **Client/Server**: The client is the terminal.  The server is the application running on the local machine.
* **Stateless**: With only a few exceptions, the program is non-interactive and does not remember previous actions / requests.  Data is persistent, however.
* **Uniform Interface**
  - Resource Identification in Requests: e.g. `./app 'show alice'` requests the resource corresponding to the person with username `alice`
  - Resource Manipulation Through Representations: e.g. Given I have a valid session token, When I request`./app 'session <token> delete'`, Then the resource to which the session token refers (a person) will have been deleted
  - Self-descriptive Messages: all requests are sent as ASCII text
  - Hypermedia As The Engine Of Application State: e.g. `./app 'home'` requests the home page, which includes links to the `login`, `join`, `create`, and `people` resources.
* **Layered System**: the `./app` script is not necessarily identical with the application server and may instead be a wrapper or a proxy for the actual application program

## Interaction Examples

The following examples depict an **explicitly non-exhaustive** subset of the behavioral requirements of the system.  The full set of requirements are expressed as Cucumber scenarios.  [Get the Cucumber scenarios](https://github.com/tamu-edu-students/csce606-statusboard-assignment/tree/main/tests) and **read them**.

### Jump to an Example
* Authentication
  + [login](#login)
  + [logout](#logout)
  + [home + session](#home-with-session-token)
  + [people + session](#people-with-session-token)
  + [show + session](#show-person-with-session-token)
* [Error Handling](#invalid-requests-or-data)
  + [invalid data](#invalid-data)
  + [invalid session token](#invalid-session-token)
  + [resource not found](#resource-not-found)
* Home Page
  + [home](#home-page)
* ICRUD
  + index ([people](#people))
  + [create](#create)
    - [join](#join)
  + read ([show](#show-person))
  + [update](#update)
    - [edit](#edit)
  + [delete](#delete)
* Search and Sort
  + search ([find](#find))
  + [sort](#sort)

### Home Page

#### Request

* `./app`
* `./app 'home'`

#### Reply

```
Welcome to the App!

login: ./app 'login <username> <password>'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
show people: ./app 'people'
```

*Note: `<attribute>` is a required value in the request.*

[top](#interaction-examples)

### Join

#### Request

`./app 'join'`

#### Reply

The `join` resource simulates (*inaccurately*) a web form.  The user supplies input to the application (entering values into form fields) via standard input.  In this example, the user will enter `pcr` for **username**, `qwertyuiop` for **password**, `qwertyuiop` again for **confirm password**, `prof. ritchey` for **name**, and `demonstrating` for **status**.

```
New Person
----------
username:
password:
confirm password:
name:
status:

[account created]
Person
------
name: prof. ritchey
username: pcr
status: demonstrating
updated: 2024-07-19 14:09:31

edit: ./app 'session rbHV55VSXgHS edit'
update: ./app 'session rbHV55VSXgHS update (name="<value>"|status="<value>")+'
delete: ./app 'session rbHV55VSXgHS delete'
logout: ./app 'session rbHV55VSXgHS logout'
show people: ./app '[session rbHV55VSXgHS ]people'
home: ./app ['session rbHV55VSXgHS']
```

*Note: the reply contains a "flash" message in square brackets.*

*Note: `[a]` is an optional value in the request. `(a|b)+` means at least one of the values must be included in the request.*

[top](#interaction-examples)

### Login

#### Request

`./app 'login pcr qwertyuiop'`

#### Reply

```
Welcome back to the App, prof. ritchey!

"demonstrating"

edit: ./app 'session rbHV55VSXgHS edit'
update: ./app 'session rbHV55VSXgHS update (name="<value>"|status="<value>")+'
logout: ./app 'session rbHV55VSXgHS logout'
people: ./app '[session rbHV55VSXgHS ]people'
```

*Note: the session token is the same as when the account was created.*

[top](#interaction-examples)

### Home (with session token)

#### Request

* `./app 'session rbHV55VSXgHS'`
* `./app 'session rbHV55VSXgHS home'`

#### Reply

```
Welcome back to the App, prof. ritchey!

"demonstrating"

edit: ./app 'session rbHV55VSXgHS edit'
update: ./app 'session rbHV55VSXgHS update (name="<value>"|status="<value>")+'
logout: ./app 'session rbHV55VSXgHS logout'
people: ./app '[session rbHV55VSXgHS ]people'
```

*Note: this is the same reply as for login, i.e. login lands on the home page.*

[top](#interaction-examples)

### People

#### Request

`./app 'people'`

#### Reply

This reply assumes there are other people also registered.

```
People
------
prof. ritchey @pcr (./app 'show pcr')
  demonstrating
  @ 2024-07-19 14:09:31
Bob @bob (./app 'show bob')
  talking to alice
  @ 2024-07-18 21:14:57
Eve @eve (./app 'show eve')
  listening to alice and bob
  @ 2024-07-18 21:14:56
Dave @dave (./app 'show dave')
  zzz
  @ 2024-07-18 21:14:55
Alice @alice (./app 'show alice')
  listening to bob
  @ 2024-07-18 21:14:54

find: ./app 'find <pattern>'
sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
home: ./app
```

[top](#interaction-examples)

### People (with session token)

#### Request

`./app 'session rbHV55VSXgHS people'`

#### Reply

```
People
------
prof. ritchey @pcr (./app 'show pcr')
  demonstrating
  @ 2024-07-19 14:09:31
  edit: ./app 'session rbHV55VSXgHS edit'
Bob @bob (./app 'show bob')
  talking to alice
  @ 2024-07-18 21:14:57
Eve @eve (./app 'show eve')
  listening to alice and bob
  @ 2024-07-18 21:14:56
Dave @dave (./app 'show dave')
  zzz
  @ 2024-07-18 21:14:55
Alice @alice (./app 'show alice')
  listening to bob
  @ 2024-07-18 21:14:54

find: ./app 'find <pattern>'
sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'
update: ./app 'session 59JwBk+kUPPr update (name="<value>"|status="<value>")+'
home: ./app ['session rbHV55VSXgHS']
```

[top](#interaction-examples)

### Edit

#### Request

`./app 'session rbHV55VSXgHS edit'`

#### Reply

The `edit` resource simulates (*inaccurately*) a web form.  The user supplies input to the application (entering values into form fields) via standard input.  In this example, the user will enter nothing for **name** (to keep the current value), and `gig 'em, aggies` for **status**.

```
Edit Person
-----------
leave blank to keep [current value]
name [prof. ritchey]:
status [demonstrating]:

[status updated]
Person
------
name: prof. ritchey
username: pcr
status: gig 'em, aggies
updated: 2024-07-19 14:29:02

edit: ./app 'session rbHV55VSXgHS edit'
update: ./app 'session rbHV55VSXgHS update (name="<value>"|status="<value>")+'
delete: ./app 'session rbHV55VSXgHS delete'
logout: ./app 'session rbHV55VSXgHS logout'
show people: ./app '[session rbHV55VSXgHS ]people'
home: ./app ['session rbHV55VSXgHS']
```

*Note: the reply contains a "flash" message in square brackets.*

*Note: the session token is the same, the updated timestamp changed.*

[top](#interaction-examples)

### Show Person

#### Request

`./app 'show pcr'`

#### Reply

```
Person
------
name: prof. ritchey
username: pcr
status: gig 'em, aggies
updated: 2024-07-19 14:29:02

people: ./app 'people'
home: ./app
```

[top](#interaction-examples)

### Show Person (with session token)

#### Request

`./app 'session rbHV55VSXgHS show pcr'`

#### Reply

```
Person
------
name: prof. ritchey
username: pcr
status: gig 'em, aggies
updated: 2024-07-19 14:29:02

edit: ./app 'session rbHV55VSXgHS edit'
update: ./app 'session rbHV55VSXgHS update (name="<value>"|status="<value>")+'
delete: ./app 'session rbHV55VSXgHS delete'
logout: ./app 'session rbHV55VSXgHS logout'
people: ./app '[session rbHV55VSXgHS ]people'
home: ./app ['session rbHV55VSXgHS']
```

[top](#interaction-examples)

### Logout

#### Request

`./app 'session rbHV55VSXgHS logout'`

#### Reply

```
[you are now logged out]
Welcome to the App!

login: ./app 'login <username> <password>'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
people: ./app 'people'
```

*Note: the reply contains a "flash" message in square brackets.*

[top](#interaction-examples)

### Find

#### Request Format

`./app 'find[ <pattern>]'`

where `<pattern>` is one of:

* `<value>` - search all fields for *value*
* `username: <value>` - search usernames for *value*
* `name: <value>` - search names for *value*
* `status: <value>` - search statuses fields for *value*
* `updated: <value>` - search timestamps for *value*

where `<value>` is any string.

#### Request

`./app 'find status: ag'`

#### Reply

```
People (find "ag" in status)
----------------------------
prof. ritchey @pcr (./app 'show pcr')
  gig 'em, aggies
  @ 2024-07-19 14:29:02

find: ./app 'find <pattern>'
sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'
people: ./app 'people'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
home: ./app
```

*Note: the search parameters are included in parentheses.*

*Note: the link for `people` is provided.*

[top](#interaction-examples)

### Sort

#### Request Format

`./app 'sort[ username|name|status|updated[ asc|desc]]'`

E.g.

* `./app 'sort'` - sort by updated in descending order (most recent first)
* `./app 'sort name'` - sort by name is ascending order (A-Z)
* `./app 'sort username desc'` - sort by username in descending order (Z-A)

#### Request

`./app 'sort name'`

#### Reply

```
People (sorted by name, a-z)
----------------------------
Alice @alice (./app 'show alice')
  listening to bob
  @ 2024-07-18 21:14:54
Bob @bob (./app 'show bob')
  talking to alice
  @ 2024-07-18 21:14:57
Dave @dave (./app 'show dave')
  zzz
  @ 2024-07-18 21:14:55
Eve @eve (./app 'show eve')
  listening to alice and bob
  @ 2024-07-18 21:14:56
prof. ritchey @pcr (./app 'show pcr')
  demonstrating
  @ 2024-07-19 14:09:31

find: ./app 'find <pattern>'
sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'
people: ./app 'people'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
home: ./app
```

*Note: the sort parameters are included in parentheses.*

*Note: the link for `people` is provided.*

[top](#interaction-examples)

### Delete

#### Request

Let `l4rPVABOIZCE` be a valid session token for user `pcr`.

`delete: ./app 'session l4rPVABOIZCE delete'`

#### Reply

```
[account deleted]
Welcome to the App!

login: ./app 'login <username> <password>'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
show people: ./app 'people'
```

*Note: the reply contains a "flash" message in square brackets.*

[top](#interaction-examples)

#### Show People After Delete

```
People
------
Bob @bob (./app 'show bob')
  talking to alice
  @ 2024-07-18 21:14:57
Eve @eve (./app 'show eve')
  listening to alice and bob
  @ 2024-07-18 21:14:56
Dave @dave (./app 'show dave')
  zzz
  @ 2024-07-18 21:14:55
Alice @alice (./app 'show alice')
  listening to bob
  @ 2024-07-18 21:14:54

find: ./app 'find <pattern>'
sort: ./app 'sort[ username|name|status|updated[ asc|desc]]'
join: ./app 'join'
create: ./app 'create username="<value>" password="<value>" name="<value>" status="<value>"'
home: ./app
```

[top](#interaction-examples)

### Create

The `create` resource is the *True* RESTful resource for creating new people.

#### Request

`./app 'create username="pcr" password="qwertyuiop" name="prof. ritchey" status="feeling creative"'`

*Note: the keyword arguments `username`, `password`, `name`, and `status` are all required but can be specified in any order.*

#### Reply

```
[account created]
Person
------
name: prof. ritchey
username: pcr
status: feeling creative
updated: 2024-07-19 15:34:26

edit: ./app 'session cFJxPl5Omzrq edit'
update: ./app 'session cFJxPl5Omzrq update (name="<value>"|status="<value>")+'
delete: ./app 'session cFJxPl5Omzrq delete'
logout: ./app 'session cFJxPl5Omzrq logout'
people: ./app '[session cFJxPl5Omzrq ]people'
home: ./app ['session cFJxPl5Omzrq']
```

[top](#interaction-examples)

### Update

The `update` resource the *True* RESTful resource for updating people.

#### Request

`./app 'session cFJxPl5Omzrq update status="feeling updated"'`

*Note: at least one of the keyword arguments `name` and `status` are required but can be specified in any order.*

#### Reply

```
[status updated]
Person
------
name: prof. ritchey
username: pcr
status: feeling updated
updated: 2024-07-19 15:37:03

edit: ./app 'session cFJxPl5Omzrq edit'
update: ./app 'session cFJxPl5Omzrq update (name="<value>"|status="<value>")+'
delete: ./app 'session cFJxPl5Omzrq delete'
logout: ./app 'session cFJxPl5Omzrq logout'
people: ./app '[session cFJxPl5Omzrq ]people'
home: ./app ['session cFJxPl5Omzrq']
```

[top](#interaction-examples)

### Invalid Requests or Data

#### Invalid Session Token

Anytime a session token is provided, it should be validated.

Suppose the token `rbHV55VSXgHS` is invalid.
Then, any request which uses that token is invalid:

* `./app 'session rbHV55VSXgHS'`
* `./app 'session rbHV55VSXgHS home'`
* `./app 'session rbHV55VSXgHS people'`
* `./app 'session rbHV55VSXgHS join'`
* `./app 'session rbHV55VSXgHS login ...'`
* and so on

```
try harder.

invalid request: invalid session token

home: ./app
```

[top](#interaction-examples)

#### Invalid Data

In the event of invalid data, e.g. invalid username during join/create, the reply should specify what action failed and why:

```
try harder.

failed to join: passwords do not match

home: ./app
```

```
try harder.

failed to create: pcr is already registered

home: ./app
```

```
try harder.

failed to update: status is too long

home: ./app
```

[top](#interaction-examples)


#### Resource Not Found

In the event of a request for a resource which does not exist, e.g. sorting by a fake attribute or requesting a fake person, the reply should specify that the resource was not found (a la HTTP 404):

```
try harder.

resource not found

home: ./app
```

[top](#interaction-examples)

### Refinements of Requirements

If you find a requirement that is not expressed completely (i.e. you can write code that passes the test but is actually wrong), you may send me a scenario of your own authorship (include the name of the feature to which it belongs) that more completely constrains acceptable solutions and I may reward you with praise or bonus points (the real reward, as we all know, is the opportunity to learn).

I am 100% certain that the requirements are not complete because I intentially left them incomplete -- at least, less complete than I could have made them -- so you could have more opportunities to learn.

## Implementation Requirements
You may use any of the following languages + unit test tools (listed in alphabetic order):

* Java + JUnit
* Python + PyTest
* Ruby + RSpec

*If you want to use a language or unit test framework/tool which is not listed, you must get approval from me (the instructor) first.  Using a language or tool without approval is grounds for receiving a 0 on this assignment.*

### Basic Requirements
Regardless of the language you use, you **must**:
* create classes / objects that represent the principal objects of the system
  + these objects must interact to produce the desired behavior of the application
  + you will probably need representations of:
    - Application - the overall application
    - Person - an individual person
    - Session - data that identifies a user with a person
* write unit tests that cover &ge; 90% of your code
  + need help with testing? [see examples of writing tests](test_examples.md)
  + need help with coverage? [see examples of using coverage tools](coverage_tool_examples.md)
* pass 100% of your own unit tests
* pass at least 70% of my [acceptance tests](https://github.com/tamu-edu-students/csce606-statusboard-assignment/tree/main/tests)
* create three (3) executable scripts `app`, `db-reset`, `test`:
  + the scripts must be **text**, i.e. written in a scripting language like bash or python
    - for bash, put `#!/usr/bin/bash` at the top
    - for python, put `#!/usr/bin/python3` at the top
  + `./app` runs the main application
    - `./app 'request'` sends a request to the application, to which the application responds by printing to the terminal
  + `./db-reset` resets the database (or whatever peristent storage mechanism you use)
    - `./db-reset` should **not** be used by your unit tests (see `./test` below)
    - and it should **not** print anything to the terminal
  + `./test` runs your unit tests against the source and reports the **passing** and **coverage** rates to the terminal.
    - the final two (2) lines of output from `test` must have format: `passing: <#>%` and `coverage: <#>%`, where `<#>` is a numeric value between 0 and 100.
      * pass rate first, followed by coverage rate
    - it must **actually run the tests and measure coverage**.  hardcoding the passing or coverage rate, such as `print('passing: 100%')` or `print('coverage: 100%')`, is an act of academic dishonesty.


## Scoring
Your score on this assignment is a function of:
* *c*: the **coverage** your tests achieve
* *a*: the **acceptance** your code acheives
* *d*: any **deductions** for lack of quality (or, worse, lack of honesty)

The score will be 0 if:
* your tests are not 100% passing, **or**
* your coverage is less than 90%, **or**
* your acceptance (scenarios **or** steps) is less than 70%

If your tests are 100% passing **and** they cover at least 90% of your code **and** your code passes at least 70% of my acceptance tests, then your score on the assignment is

**score**(*c*, *a*, *d*) = *c* + *a* - (*d* + 100),

where *a* = 50 &times; (*a<sub>scenarios</sub>* + *a<sub>steps</sub>*) and *a<sub>X</sub>* = *X<sub>passed</sub>* / *X<sub>total</sub>*.


Any deductions will be applied during manual review of your submission.

You will submit your work to [gradescope](https://www.gradescope.com/) (see [Submission](#submission), below). The autograder on gradescope will:

1. invoke `./test` and look for `passing: <#>%` and `coverage: <#>%` on the last two (2) lines of output. Your last two (2) lines of output must be *exactly* `passing: <#>%\ncoverage: <#>%`, where `<#>` is a number (could be whole like `97` or could have a fractional part like `89.99` but must be decimal).  Failure to produce those two (2) lines of output will result in a score of 0 for the submission (you must fix it and re-submit).
2. invoke `cucumber` to run the acceptance tests and check the number of scenarios and steps passed
   + your code must pass at least 70% of **each** to be accepted, otherwise the score will be 0 for the submission (you must fix it and re-submit)

You may submit as many times as you like before the due date.
Your **last** submission is the one that is recorded.

**Note**: The instructional team (instructor, TA(s), and graders(s)) will be manually reviewing submissions for "Quality" and "Honesty".

| Item | Description |
| --- | --- |
| Quality | Weak tests, hacky solutions, and disorganiztion are just a few of the many ways code can lack quality.  We don't expect you to write beautiful code (yet), but we do expect you to be able to write reasonably good code (specifically: **readable** code).  Keeping your code well-organized, naming your classes, methods, and variables appropriately, and striving to write a strong and robust test suite will help you to write high-quality code. |
| Honesty | Write your own code and keep your tests relevant and your reporting accurate.  Any evidence of academic dishonesty will result in an academic honesty violation report (see Academic Honesty below). |

## Dependencies
The autograding container on gradescope currently has the following relevant tools and libraries / packages / modules:

| command    | tool version |
| -------    | ------------ |
| `bundler`  | 2.5.17       |
| `coverage` | 7.6.1        |
| `cucumber` | 9.2.0        |
| `gem`      | 3.5.9        |
| `java`     | 17.0.12      |
| `javac`    | 17.0.12      |
| `jq`       | 1.6          |
| `mvn`      | 3.9.8        |
| `pytest`   | 8.3.2        |
| `python3`  | 3.10.12      |
| `rspec`    | 3.13         |
| `rubocop`  | 1.65.0       |
| `ruby`     | 3.3.2        |

| lib / pkg / module / etc. | version |
| ------------------------- | ------- |
| PyHamcrest                | 2.1.0   |
| pytest-cov                | 5.0.0   |
| pytest-mock               | 3.14.0  |

<sup>*Last Updated: 14:35 7 August 2024*</sup>

If your submission has package / library dependencies that are not on that list, you must send me *concise* instructions for automatically installing them at least 72 hours (3 days) before the due date.  Failure to do so may result in your submission(s) being ungradeable (i.e. assigned a score of 0).

Please keep your dependencies to a minimum.  If you have an esoteric (or otherwise uncommon dependency), you are probably overthinking the problem.

An example of acceptably concise instructions:

> Howdy Prof. Ritchey,
>
> I need `cowsay` for PA 0.  To install, run `apt-get install cowsay`.
>
> Thank you!

## Submission
You must submit to [gradescope](https://www.gradescope.com/) the following files:
* source code (e.g. class definitions for all system components)
* the `app` script (the file must be named *exactly* `app`)
* the `db-reset` script (the file must be named *exactly* `db-reset`)
* the `test` script (the file must be named *exactly* `test`)

The ultimate directory structure of your submission is mostly up to you.  The only requirement is that `app`, `db-reset`, and `test` be in the root (top-level directory) of your submission, e.g.

```
submission.zip
|- src/
|  |- main/
|  |  |- java/
|  |  |  |- app/
|  |  |  |  |- App.java
|  |  |  |  |- Person.java
|  |- test/
|  |  |- java/
|  |  |  |- app/
|  |  |  |  |- AppTest.java
|  |  |  |  |- PersonTest.java
|- app
|- db-reset
|- pom.xml
|- test
```

## Academic Honesty
I explicitly expect that you will **do your own work** and will **not attempt to subvert or circumvent** the requirements of this assignment.  I think this assignment will be valuable for your learning.  Attempting to avoid doing it honestly detracts from that value.

Academic dishonesty **will** result in an academic honesty violation report with a recommendation of F* in the course.
This includes, but is not limited to:
* **cheating**: intentionally using or attempting to use unauthorized materials, information, notes, study aids or other devices or materials in any academic exercise. Unauthorized materials may include anything or anyone that gives a student assistance and has not been specifically approved in advance by the instructor.
* **fabrication**: making up data or results, and recording or reporting them; submitting fabricated documents.
  + e.g. forging coverage data; reporting false coverage rate, reporting a hardcoded coverage rate
* **plagiarism**: the appropriation of another person's ideas, processes, results, or words without giving appropriate credit.
  + e.g. copying any amount of code from someone else
* **complicity**: intentionally or knowingly helping, or attempting to help, another to commit an act of academic misconduct.
  + e.g. allowing someone else to copy any amount of code from you
* **falsification**: manipulating research and/or academic materials, documentation, equipment, or processes; changing or omitting data or results such that the research or information is not accurately represented in the research or academic record.
  + e.g. manipulating coverage data
* abuse and misuse of access and unauthorized access
  + e.g. "hacking" the autograder or gradescope
* violation of university, college, program, departmental, or course rules

You should refer to the [Honor System Rules](https://aggiehonor.tamu.edu/Rules-and-Procedures/Rules/Honor-System-Rules) and/or the instructor for more information and clarification, if necessary.
