---
title: 'eft + eftcmdr: dialog boxes w/ ruby, yaml and whiptail'
category: dev
tags:
- dev
- lib
- ruby
- eft
- eftcmdr

<style scoped> img[src*="eftcmdr"] { width: 150px; } </style>

I've created two ruby gems that provide DSLs for
[whiptail](https://en.wikipedia.org/wiki/Newt_(programming_library)).

### [eft](https://github.com/obfusk/eft)

Provides a ruby DSL:

```ruby
Eft.ask('What is your name?') do |q|
  q.on_ok { |name| puts "Hello, #{name}!" }
end
```

### [eftcmdr](https://github.com/obfusk/eftcmdr)

Provides a yaml DSL:

```yaml
ask:    ask_name
text:   What is your name?
then:
  eval: eval_hello
  code: |
    puts "Hello, #{ctx[:ask_name]}!"
```

```bash
$ eftcmdr examples/hello.yml
```

And can, for example, be used to provide a menu over `ssh`.

[![hello](/img/eftcmdr_1_hello.png)](/img/eftcmdr_1_hello.png)
[![apps](/img/eftcmdr_2_apps.png)](/img/eftcmdr_2_apps.png)
[![commands](/img/eftcmdr_3_commands.png)](/img/eftcmdr_3_commands.png)
[![output](/img/eftcmdr_4_output.png)](/img/eftcmdr_4_output.png)
[![confirm](/img/eftcmdr_5_confirm.png)](/img/eftcmdr_5_confirm.png)

<br/> \- Felix

&rarr; [Comments](https://github.com/obfusk/obfusk.github.io/issues/2)
