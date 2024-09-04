# Examples of Testing in Java, Python, and Ruby

[back to main page](README.md)

There are **many** frameworks and tools for testing in each of these languages.  Here, I will show you just one for each.  You are essentially required to use one of these frameworks/tools for testing (because testing by hand/eye is too tedious).

## Basic Testing
Given the level of this course, I expect that you already have some experience with testing.  At the very least, you should understand the basics of testing.

> The general idea of testing is to **have an expectation of correct behavior** and then **verify it**.

There is a simple technique which works for all languages, but it's more work (because there's no *a priori* framework or tool... you build the framework and tools yourself).  This is what most testing frameworks and tools have already done for you, enabling you to focus on expressing the expectations while the tool takes care of all the low-level details (whoop for abstraction, y'all!).

1. **Given** *&lt;preconditions&gt;*
   * set up the program state for the test
2. **When** *&lt;actions&gt;*
   * perform the action, invoke the methods, present the stimulus, etc.
3. **Then** *&lt;postconditions&gt;*
   * verify that the expected behavior occurred, the correct value was returned, etc.

For example,

> **Given** Rational numbers `a = 1/2` and `b = 1/3`
>
> **When** I compute `c = a + b`
>
> **Then** `c` should be `5/6`

### Psuedocode (general case)

```
// Given the value(s) of args
args = ...
// When I do action foo
actual = foo(args)
// Then the expected behavior should happen
if actual != expected
  print "[FAIL] expected foo(args) to be {expected}, got {actual}."
end-if
```

### Java
```java
// Given ...
Rational a = new Rational(1, 2);
Rational b = new Rational(1, 3);
// When ...
Rational c = a.plus(b);
// Then ...
if (!(c.equals(new Rational(5, 6)))) {
  System.out.println("[FAIL] expected 1/2 + 1/3 to be 5/6");
}
```

### Python
```python
# Given ...
a = Rational(1, 2)
b = Rational(1, 3)
# When ...
c = a + b
# Then ...
if c != Rational(5, 6)
    print('[FAIL] expected 1/2 + 1/3 to be 5/6')
```

### Ruby
```ruby
# Given ...
a = Rational.new(1, 2)
b = Rational.new(1, 3)
# When ...
c = a + b
# Then ...
if c != Rational.new(5, 6)
  puts '[FAIL] expected 1/2 + 1/3 to be 5/6'
end
```

## Advanced Testing
Hopefully, you have used some advanced testing framework in the past.  Here are three-ish, one-ish for each language, that I recommend using.

### Java
Use [JUnit 5](https://junit.org/junit5/).

This example also uses [Hamcrest](https://hamcrest.org/JavaHamcrest/) matchers (which I quite like).

```java
package rational;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

import org.junit.jupiter.api.Test;

class RationalTest {

  @Test
  void testExampleTest() {
    Rational a = new Rational(1, 2);
    Rational b = new Rational(1, 3);
    Rational c = a.plus(b);
    assertThat(c, equalTo(new Rational(5, 6)));
  }
}
```

### Python
Use [pytest](https://docs.pytest.org/en/7.4.x/).

```python
from rational import Rational

class TestRational:
    def test_example(self):
        a = Rational(1, 2)
        b = Rational(1, 3)
        c = a + b
        assert c == Rational(5, 6)
```

### Ruby
Use [RSpec](https://rspec.info).

```ruby
require 'rational'

RSpec.describe Rational, "#+" do
  it 'adds 1/2 and 1/3' do
    a = Rational.new(1, 2)
    b = Rational.new(1, 3)
    c = a + b
    expect(c).to eql(Rational.new(5, 6))
  end
end
```
