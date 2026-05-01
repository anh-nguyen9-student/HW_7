ECE 479/579 Spring 2026
Final Project/Exam
Due: May 8th, 2026 11:59pm via D2L
Documents to be submiIed:
1. Project report
2. Code (in C/C++, Python)
3. InstrucRons to run your system
You are to design an AI expert system FOODIE (Food Intelligence Electrified) to run a network of
food delivery robots in a locale (e.g., a university campus). In what follows, broad requirements
are given with specific goals. Your task is to refine them as you see fit and most appropriate to
make such as a system as automated, eﬃcient, and smart as possible. You have a “creaRve
license” to propose an interesRng soluRon.
My iniHal assumpHons are:
1. 2. 3. 4. The locale is a known bounded terrain. More specifically, it has pathways for the robots
to move about. Robots may encounter obstacles along pathways. Such obstacles may
not be known a priori.
There is a finite number of movable robots, each equipped with HW/SW and
“intelligence” that can be as complex as you will desire for it to be. In addiHon, robots
have compartments, and a roboHc arm that allows them to pick and bag items and place
bags in the compartments.
Robots will depart from and return to a food warehouse (FW) in which they:
a. Park and recharge.
b. Receive orders for food items.
c. Bag the items.
d. May deliver more than one order to more than one locaHon and then return to
the FW.
e. Load up the items into their compartment.
Once a robot has configured and loaded the order, it departs to the desHnaHon specified
in the order.
Propose the design of FOODIE (and implement some of its aspects as required below) with the
following goals:
A OpRmize the routes that the robots take based on the orders received.
For this goal, select or propose an algorithm that minimizes delivery Hme and minimizes energy
consumpHon by robots. Consider potenHal for replanning the route as robots may encounter
small or intractable obstacles (for instance, a pathway closed to traﬃc due to construcHon).
Please remember that you have more than one robot and several of them can deliver several
orders concurrently.
For this task, implement your soluHon and demonstrate it on a small simulaHon.
B Propose an expert module to bag (FOODIE_BAGGER) the food items into a robot’s
compartment.
FOODIE will have a rule-based system that will decide where each item from the order will go.
Specifically, a) the bag large items step will load large items first (for instance, big bo\les of
water), b) the bag medium items step will load medium items next, and c) bag small items step
will be next. Assume that frozen items need freezer bags. Other items need paper bags of equal
size but clearly capable of only accommodaHng a finite number of items, depending on the
items’ sizes.
A rule might have the following form:
R: if step is bag-medium items
there is a medium item.
the current bag contains < 10 items.
then add this item to the bag.
Your rules should make sure that fragile items do not get crushed in a bag.
Run a simulaHon of this rule-based system for a small order, for example, 2 x 1-gallon bo\les of
water, pint of ice cream, granola box, loaf of bread. (Make up your own order as input). A
sample trace of your simulaHon might look as follows:
Rule Ri says: Rule Rk says: Rule Rm says: Rule Rx says: Rule Ry says: Bag lager items.
Put 1 gallon water bottle in bag_1.
Put watermelon in bag_1.
Start a new bag.
Put ice cream in a freezer bag.
…
…
C Propose an expert system module (FOODIE_Springs_to_AcRon: Foodie_SPA) to save you
when guests show up unexpectedly at your house.
Design a backward chaining system and a small a\endant rule base for selecHng the right
beverage for your guests, that needs to be added to the order . Imagine that in general, the
beverages can be water, juice, wine, beer, liquor, with specific brands for each type for example
Corona beer, or carrot juice (if guest is a health nut and guest has allergies to citrus, then choose
carrot juice).
Foodie_SPA will take your hypothesis (for instance, “shall I serve carrot juice?”), backward chain
through the rule base and if needed, will ask you for facts that you know to be true (for
example, guest is not well liked, entre is chicken, it’s New Year’s Eve).
Implement such a system (no more than 15 rules) and show its operaHon on your own example.
A trace of execuHon might look as follows.
Trying to establish CHOOSE Polish Vodka using rule Rx
Trying to establish LIQUOR is indicated using Rm
Rule Rm fails to establish LIQUOR is indicated.
….
….
CHOOSE Dos Equis is True.
IMPORTANT: FOR IMPLEMENTATION, YOU HAVE A CHOICE TO EITHER IMPLEMENT FOODIE_BAGGER
OR FOODIE_SPA. HOWEVER, YOU HAVE TO DEVELOP RULE BASES FOR BOTH AND INCLUDE THEM IN
YOUR REPORT.
D Show how the robot would use its arm to load the bags into its compartment.
Use STRIPS basic rules or modified rules to describe the process and what acHons should be in
place in case the order has to be modified by last minute change (i.e., unexpected guests
arrive). You need not to encode this part.
Report
Your report need not be long and elaborate. In it, I expect you to state your own assumpHons in
addiHons to mine, requirements, the system’s architecture, the algorithms and methods
selected, rule bases, and STRIPS rules for secHon D. In the appendix, please a\ach sample runs
for secHons (A and B) or (A and C) as you have a choice of implemenHng either B or C.
Use of AI tools: you can use AI tools to help with refining the requirements, system architecture
and algorithms, rule-bases, and code. Please indicate which parts of your design and
implementaHon was automated, and indicate how you interacted with the tools, iterated
through the design to arrive at the final product.
