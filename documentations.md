## Week 13/09:

* Merge 2 repos into 1:
    - Refac
* New:
    - UpdateRunner as wrapper
    - Integrate Update within horn-pddl

#### Integration:

* In main compiler: UpdateRunner compute cl(T)
    - Extend the OG domain

* Later in compilation: UpdateRunner returns rules

=> Separation between 2 level; Easier Timer for Eval


* Week 28/10:

- BUG FIX IN RULE, TIME CONSUMING SINCE repr MSUT BE CHECKED BY HAND


## PROBLEM 15 WITH DOMAIN 15 TRYOUT

### 1. State

* Fact: cat(ac); contains(ao,ac);

* 1. Rule app:
    - datalogpackage(ao) :- exists.ac: contains(ao,ac)

* Fact: cat(ac); contains(ao,ac); datalogpackage(ao);

* Action:
    -> let_the_cats_out (datalogpackage, not updating)

### 2. State

* Added from effect of action: delcontainsrequest(ao,ac); insdisarmedrequest(ao);

* Fact: cat(ac); contains(ao,ac); datalogpackage(ao); datalogquery1(ao, ac); delcontainsrequest(ao,ac); insdisarmedrequest(ao);

* 1. Rule app:
    - updating :- delcontainsrequest(ao, ac);

* Fact: cat(ac); contains(ao,ac); datalogpackage(ao); delcontainsrequest(ao,ac); insdisarmedrequest(ao); updating;

* 2. Rule app:
    - delcontains(ao, ac) :- contains(ao,ac), delcontainsrequest(ao,ac)
    - insdisarmed(ao) :- insdisarmedrequest(ao), not disarmed(ao)

* Fact: cat(ac); contains(ao,ac); datalogpackage(ao); delcontainsrequest(ao,ac); insdisarmedrequest(ao); updating; delcontains(ao, ac); insdisarmed(ao);

* 3. Rule app:
    - insobjectxclosure(ac) :- delcontains(ao, ac), ...
    - inspackageclosure(ao) :- delcontains(ao, ac),...

* Fact: cat(ac); contains(ao,ac); datalogpackage(ao); delcontainsrequest(ao,ac); insdisarmedrequest(ao); updating; delcontains(ao, ac); insdisarmed(ao); insobjectxclosure(ac); inspackageclosure(ao);

* 4. Rule app:
    - inspackage(ao) :- inspackageclosure(ao)
    - insobjectx(ac) :- insobjectxclosure(ac)

* Fact: cat(ac); contains(ao,ac); datalogpackage(ao); delcontainsrequest(ao,ac); insdisarmedrequest(ao); updating; delcontains(ao, ac); insdisarmed(ao); insobjectxclosure(ac); inspackageclosure(ao); inspackage(ao); insobjectx(ac);

* Action:
    -> update

### 3. State

BEFORE: cat(ac); contains(ao,ac); datalogpackage(ao); delcontainsrequest(ao,ac); insdisarmedrequest(ao); updating; delcontains(ao, ac); insdisarmed(ao); insobjectxclosure(ac); inspackageclosure(ao); inspackage(ao); insobjectx(ac);

AFTER: cat(ac), datalogpackage(ao); package(ao); objectx(ac); disarmed(ao); datalogpackage(ao);

forall.x: (disarmed(x) or not(package(x)))


## TODO:

* Delete not needed rules
* Actions
* IF DOESNT WORK
    - FURTHER DELETION OF RULE?
* TRY WITH OTHER DOMAINS
* Complexity of planning:
    - 1 Step planning
    - Constant update action in the middle
