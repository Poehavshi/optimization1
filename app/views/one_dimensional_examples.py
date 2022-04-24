import logging

import hydra
import streamlit as st
from omegaconf import DictConfig
import matplotlib.pyplot as plt
import numpy as np

from ..controllers.one_dimensional_methods import find_min_by_gold, find_min_by_fibonacci, find_min_by_dichotomy
from collections import namedtuple
from app.models.one_dimensional_functions import f1, f2, f3, f4, TestCase

log = logging.getLogger(__name__)

case = namedtuple('TestCase', ['a', 'b', 'f'])
#                  a    b   f
test_cases = (TestCase(-10, 10, f1),
              TestCase(-2, 3, f2),
              TestCase(-2, 2, f3),
              TestCase(-10, 10, f4))


def one_argument_form(config: DictConfig):
    st.title("Functions of one argument")
    methods = [find_min_by_dichotomy, find_min_by_gold, find_min_by_fibonacci]

    test_case = st.selectbox("Function to optimize", test_cases, format_func=lambda x: f"[{x.a},{x.b}] {x.f.__doc__}")
    method = st.selectbox("Optimization method", methods, format_func=lambda x: x.__name__)

    result, iterations = method(test_case.a, test_case.b, test_case.f, epsilon=config.epsilon,
                                precision=config.precision, n=config.N)

    st.write(f"Minimum of function = {result}")
    st.write(f"Number of iterations = {iterations}")

    st.pyplot(create_plot(test_case))


def create_plot(test_case):
    x = np.linspace(test_case.a, test_case.b, 100)
    y = np.vectorize(test_case.f)(x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    return fig


if __name__ == '__main__':
    one_argument_form(hydra.compose(config_name="config"))
