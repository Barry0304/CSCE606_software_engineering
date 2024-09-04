# Ruby Version Control on MacBook

This solution is from a 606 student for Ruby version 3.2.2.

---

To address the Ruby version control problem, I utilized the `chruby` version tool.

[This comprehensive guide to Install Ruby with Chruby](https://mac.install.guide/ruby/12.html) provided step-by-step instructions that allowed me to effectively manage Ruby versions on my MacBook, ensuring compatibility with our project requirements.
With `chruby`, I was able to switch between different Ruby versions seamlessly, eliminating the issues I previously encountered.

In addition to the Ruby version control, I also made an update to my `.zshrc` profile, which further enhanced the compatibility of my development environment.

```sh
source /opt/homebrew/opt/chruby/share/chruby/chruby.sh
source /opt/homebrew/opt/chruby/share/chruby/auto.sh
chruby ruby-3.2.2
export PATH="$HOME/.gem/ruby/3.2.0/bin:$PATH"
```

I hope this will allow others to install the latest version of ruby and work effortlessly on their mac terminal.
