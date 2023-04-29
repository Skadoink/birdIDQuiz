import backend

testBE = backend.QuizBuilder(['magpet1', 'snopet1', 'nezkak1', 'kea1', 'gagcoc1', 'shoebi1'], 5)
print([(q.imageURL, q.speccode, q.species_options) for q in testBE.questions])