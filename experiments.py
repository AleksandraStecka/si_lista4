from classifiers import multinomial_naive_bayes_cross_val, support_vector_machine_cross_val


def test():
    print("-------------------------------------------------------------------------- ALPHA", end="\n\n")
    test_alpha()
    print("------------------------------------------------------------------------------ C", end="\n\n")
    test_c()
    print("--------------------------------------------------------------------------- LOSS", end="\n\n")
    test_loss()


def test_alpha():
    alpha_params = [0, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
    for alpha in alpha_params:
        print("-------------------------------------------------------------------------- " + str(alpha))
        multinomial_naive_bayes_cross_val(True, 0.5, 0.001, 5000, (1, 3), alpha)


def test_c():
    c_params = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]
    for c in c_params:
        print("-------------------------------------------------------------------------- " + str(c))
        support_vector_machine_cross_val(True, 0.5, 0.001, 5000, (1, 3), c, 'squared_hinge')


def test_loss():
    loss_params = ['hinge', 'squared_hinge']
    for loss in loss_params:
        print("-------------------------------------------------------------------------- " + loss)
        support_vector_machine_cross_val(True, 0.5, 0.001, 5000, (1, 3), 0.1, loss)
