"""
For testing the quizbuilder
"""

import backend

testBE = backend.QuizBuilder(
    ["magpet1", "snopet1", "nezkak1", "kea1", "gagcoc1", "shoebi1"], 5
)
print([(q.imageURL, q.speccode, q.species_options) for q in testBE.questions])

"""
For making a dictionary from the eBird taxonomy CSV file with common name as key and species code as value
"""
