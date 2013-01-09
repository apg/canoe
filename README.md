# Canoe - a simple (but effective), real-time log analyzer

## Description

Canoe is a simple log analyzer that watches logs and performs actions on
them in real time. It's an old concept, but a new tool.

## Concepts

### Canoes

Canoes are the processes created via chisels (filters) that are sent down a 
route (actions).

### Chisels

When you think of how you monitor log files it's likely that you sling
together a huge pipeline of shell commands--something like this

    tail -F t.log | grep '^|ERROR' --color=always | egrep -v '(ignore1|ignore2|ignore3)'
    
Which will highlight ERROR and filter out all of the ignored things. It can
get much more complicated, especially when you try to take into consideration
multiple lines and context.

In canoe, think of chisels as `grep`. Well, `grep` with an always available
`-C <n>`

Chisels can be composed, and should be for complicated tasks. 

### Routes

Routes are what happens after messages are filtered. Lets say that you
wanted to recreate the above pipeline. To do so you'd create a canoe 
out of a FilterOutWords, and send it down a ColoredOutputRoute, with
a regex to color the word 'ERROR'.

Of course, all of this is done through a configuration file, so it's
relatively easy to do.
