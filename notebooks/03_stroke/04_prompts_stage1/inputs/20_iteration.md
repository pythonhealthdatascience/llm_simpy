append new code to the end of four methods in `AcuteStrokeUnit` postfixed with "acute_treatment": if `post_asu_destination` is "Rehab" then a.) incrememnt `rehab_unit.occupancy` and then b.) call the `rehab_unit` function with the same patient_type as a simpy process.  For example, `stroke_patient_generator` called `rehab_unit.stroke_rehab_treatment`. Do not pass any parameters. The code should be located after "self.occupancy -= 1". Do not use the yield keyword.  

Display all code in the  `AcuteStrokeUnit class including all treatment and patient generator methods.


