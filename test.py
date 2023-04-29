import backend

testBE = backend.QuizBuilder(['magpet1', 'snopet1'], 5)
print([(q.imageURL, q.speccode, q.species_options) for q in testBE.questions])