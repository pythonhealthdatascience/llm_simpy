Create a new simpy generator function called `audit_rehab_occupancy` that accepts parameters: `env`, `first_interval`, `audit_interval`, an instance of the `RehabilitationUnit` called `rehab_unit`, and an instance `Experiment` called experiment. Function logic:


1. Wait `first_interval` time units 
2. The function repeatedly records the occupancy of `rehab_unit` and then waits `audit_interval` time units.  The occupancy is appended `rehab_occupancy` in the experiment class. Do not append env.now

Create a copy of the function called `audit_asu_occupancy`, but replace `rehab_unit` with `asu` and append to `asu_occupancy`

