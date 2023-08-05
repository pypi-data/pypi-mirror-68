import random

import numpy as np
import plotly
import plotly.graph_objs as go
from scipy.special import expit

from pyrvea.EAs.PPGA import PPGA
from pyrvea.Population.Population import Population
from pyrvea.Problem.baseproblem import BaseProblem


class EvoDN2(BaseProblem):
    """Creates Deep Neural Networks (DNN) for the EvoDN2 algorithm.

    DNNs have a fixed number of subnets, each of which has a random number of
    layers, and a random number of nodes in each layer, dependant on max layers
    and max nodes set by user.

    Notes
    -----
    The algorithm has been created earlier in MATLAB, and this Python implementation
    has been using
    that code as a basis.

    Python code has been written by Niko Rissanen under the supervision of professor
    Nirupam Chakraborti.

    Parameters
    ----------
    name : str
        Name of the problem
    X_train : ndarray
        Training data input
    y_train : ndarray
        Training data target values
    num_of_objectives : int
        The number of objectives
    num_samples : int
        The number of data points, or samples.
    subsets : array_like
        A list of variables used for each subnet of the model.
    params : dict
        Parameters for the models

    References
    ----------
    [1] Swagata R., Bhupinder S., Chakrabarti, N. and Chakraborti, N. (2019). A new
    Deep Neural Network algorithm
    employed in the study of mechanical properties of micro-alloyed steel.
    Department of Metallurgical and Materials Engineering, Indian Institute of
    Technology.
    """

    def __init__(
        self,
        name=None,
        X_train=None,
        y_train=None,
        num_of_objectives=2,
        num_samples=None,
        subsets=None,
        params=None,
    ):
        super().__init__()

        self.name = name
        self.X_train = X_train
        self.y_train = y_train
        self.num_of_objectives = num_of_objectives
        self.num_samples = num_samples
        self.subsets = subsets
        self.params = params

    def objectives(self, decision_variables) -> list:
        """ Use this method to calculate objective functions.

        Parameters
        ----------
        decision_variables : ndarray
            Variables from the neural network
        Returns
        -------
        obj_func : list
            The objective function
        """

        non_linear_layer, complexity = self.activation(decision_variables)
        _, predicted_values, training_error = self.calculate_linear(non_linear_layer)

        obj_func = [training_error, complexity]

        return obj_func

    def activation(self, decision_variables):
        """ Calculates the dot product and applies the activation function.
        Parameters
        ----------
        decision_variables : ndarray
            Array of all subnets in the current neural network

        Returns
        -------
        non_linear_layer : ndarray
            The final non-linear layer before the output
        complexity : float
            The complexity of the neural network
        """
        network_complexity = []
        non_linear_layer = np.empty((self.num_samples, 0))

        for i, subnet in enumerate(decision_variables):

            # Get the input variables for the first layer
            in_nodes = self.X_train[:, self.subsets[i]]
            subnet_complexity = 1

            for layer in subnet:
                # Calculate the dot product + bias
                out = np.dot(in_nodes, layer[1:, :]) + layer[0]

                subnet_complexity = np.dot(subnet_complexity, np.abs(layer[1:, :]))

                in_nodes = self.activate(self.params["activation_func"], out)

            network_complexity.append(np.sum(subnet_complexity))
            non_linear_layer = np.hstack((non_linear_layer, in_nodes))

        complexity = np.sum(network_complexity)

        return non_linear_layer, complexity

    def calculate_linear(self, activated_layer):
        """ Apply the linear function to the final output layer
        and calculate the training error.

        Parameters
        ----------
        activated_layer : ndarray
            Output of the activation function.

        Returns
        -------
        linear_layer : ndarray
            The optimized output layer of the network.
        predicted_values : ndarray
            The prediction of the model.
        training_error : float
            Training error of the model.
        """

        linear_layer = None
        predicted_values = None
        training_error = None

        if self.params["opt_func"] == "llsq":
            linear_solution = np.linalg.lstsq(activated_layer, self.y_train, rcond=None)
            linear_layer = linear_solution[0]
            predicted_values = np.dot(activated_layer, linear_layer)

        if self.params["loss_func"] == "root_mean_square":
            training_error = np.sqrt(np.mean(((self.y_train - predicted_values) ** 2)))

        elif self.params["loss_func"] == "root_median_square":
            training_error = np.sqrt(
                np.median(((self.y_train - predicted_values) ** 2))
            )

        return linear_layer, predicted_values, training_error

    def select(self, pop, non_dom_front, selection="min_error"):
        """ Select target model from the population.

        Parameters
        ----------
        pop : obj
            The population object.
        non_dom_front : list
            Indices of the models on the non-dominated front.
        selection : str
            The criterion to use for selecting the model.
            Possible values: 'min_error', 'manual'

        Returns
        -------
        model:
            The selected model.
        fitness:
            The model's fitness values.

        """
        model = None
        fitness = None
        if selection == "min_error":
            # Return the model with the lowest error

            lowest_error = np.argmin(pop.objectives[:, 0])
            model = pop.individuals[lowest_error]
            fitness = pop.fitness[lowest_error]

        elif selection == "manual":

            pareto = pop.objectives[non_dom_front]
            hover = pop.objectives[non_dom_front].tolist()

            for i, x in enumerate(hover):
                x.insert(0, "Model " + str(non_dom_front[i]) + "<br>")

            trace0 = go.Scatter(
                x=pop.objectives[:, 0], y=pop.objectives[:, 1], mode="markers"
            )
            trace1 = go.Scatter(
                x=pareto[:, 0],
                y=pareto[:, 1],
                text=hover,
                hoverinfo="text",
                mode="markers+lines",
            )
            data = [trace0, trace1]
            layout = go.Layout(
                xaxis=dict(title="training error"), yaxis=dict(title="complexity")
            )
            plotly.offline.plot(
                {"data": data, "layout": layout},
                filename=self.name + "_training_models_" + "pareto" + ".html",
                auto_open=True,
            )

            model_idx = None
            while model_idx not in non_dom_front:
                usr_input = input(
                    "Please input the number of the model of your preference: "
                )
                try:
                    model_idx = int(usr_input)
                except ValueError:
                    print("Invalid input, please enter the model number.")
                    continue

                if model_idx not in non_dom_front:
                    print("Model " + str(model_idx) + " not found.")

            model = pop.individuals[int(model_idx)]
            fitness = pop.fitness[int(model_idx)]

        return model, fitness

    @staticmethod
    def activate(name, x):
        if name == "sigmoid":
            return expit(x)

        if name == "relu":
            return np.maximum(x, 0)

        if name == "tanh":
            return np.tanh(x)


class EvoDN2Model(EvoDN2):
    """Class for the EvoDN2 surrogate model.

    Parameters
    ----------
    model_parameters : dict
        Parameters passed for the model.
    ea_parameters : dict
        Parameters passed for the genetic algorithm.

    Attributes
    ----------
    name : str
        Name of the problem
    subnets : array_like
        A list containing the subnets of the model.
    subsets : array_like
        A list of variables used for each subnet of the model.
    fitness : list
        Fitness of the trained model.
    non_linear_layer : np.ndarray or None
        The activated layer combining all of the model's subnets.
    linear_layer : np.ndarray or None
        The final optimized layer of the network.
    svr : array_like
        Single variable response of the model.
    log : file
        If logging set to True in params, external log file is stored here.

    """

    def __init__(self, model_parameters=None, ea_parameters=None):
        super().__init__()
        self.name = "EvoDN2_Model"
        self.subnets = None
        self.subsets = None
        self.fitness = []
        self.non_linear_layer = None
        self.linear_layer = None
        self.svr = None
        self.log = None
        self.ea_params = ea_parameters
        if model_parameters:
            self.set_params(**model_parameters)
        else:
            self.set_params()

    def set_params(
        self,
        name="EvoDN2_Model",
        training_algorithm=PPGA,
        pop_size=500,
        num_subnets=4,
        max_layers=4,
        max_nodes=4,
        prob_omit=0.2,
        w_low=-5.0,
        w_high=5.0,
        activation_func="sigmoid",
        opt_func="llsq",
        loss_func="root_mean_square",
        selection="min_error",
        recombination_type="evodn2_xover_mutation",
        crossover_type="standard",
        mutation_type="gaussian",
        logging=False,
        plotting=False,
    ):
        """ Set parameters for EvoDN2 model.

        Parameters
        ----------
        name : str
            Name of the problem.
        training_algorithm : EA
            Which training algorithm to use.
        pop_size : int
            Population size.
        num_subnets : int
            Number of subnets.
        max_layers : int
            Maximum number of hidden layers in each subnet.
        max_nodes : int
            Maximum number of nodes in each hidden layer.
        prob_omit : float
            Probability of setting some weights to zero initially.
        w_low : float
            The lower bound for randomly generated weights.
        w_high : float
            The upper bound for randomly generated weights.
        activation_func : str
            Function to use for activation.
        opt_func : str
            Function to use for optimizing the final layer of the model.
        loss_func : str
            The loss function to use.
        selection : str
            The selection to use for selecting the model.
        recombination_type, crossover_type, mutation_type : str
            Recombination functions. If recombination_type is specified, crossover and
            mutation
            will be handled by the same function. If None, they are done separately.
        logging : bool
            True to create a logfile, False otherwise.
        plotting : bool
            True to create a plot, False otherwise.

        """
        params = {
            "name": name,
            "training_algorithm": training_algorithm,
            "pop_size": pop_size,
            "num_subnets": num_subnets,
            "max_layers": max_layers,
            "max_nodes": max_nodes,
            "prob_omit": prob_omit,
            "w_low": w_low,
            "w_high": w_high,
            "activation_func": activation_func,
            "opt_func": opt_func,
            "loss_func": loss_func,
            "selection": selection,
            "crossover_type": crossover_type,
            "mutation_type": mutation_type,
            "recombination_type": recombination_type,
            "logging": logging,
            "plotting": plotting,
        }

        self.name = name
        self.params = params

    def fit(self, training_data, target_values):
        """Fit data in EvoDN2 model, divide input variables for each subnet randomly,
        and train the model.

        Parameters
        ----------
        training_data : pd.DataFrame, shape = (numbers of samples, number of variables)
            Training data.
        target_values : pd.DataFrame
            Target values.

        Returns
        -------
        self : returns an instance of self.

        """
        self.X_train = np.asarray(training_data)
        self.y_train = np.asarray(target_values)
        self.num_samples = target_values.shape[0]
        self.num_of_variables = training_data.shape[1]

        self.subsets = []

        # Create random subsets of decision variables for each subnet

        for i in range(self.params["num_subnets"]):
            n = random.randint(1, self.X_train.shape[1])
            self.subsets.append(random.sample(range(self.X_train.shape[1]), n))

        # Ensure that each decision variable is used as an input in at least one subnet
        for n in list(range(self.X_train.shape[1])):
            if not any(n in k for k in self.subsets):
                self.subsets[random.randint(0, self.params["num_subnets"] - 1)].append(
                    n
                )

        self.train()

        self.single_variable_response(ploton=self.params["plotting"])

        if self.params["logging"]:
            self.create_logfile()

        return self

    def train(self):
        """
        Create a random population, evolve it and select a model based on selection.
        """
        pop = Population(
            self,
            assign_type="EvoDN2",
            pop_size=self.params["pop_size"],
            recombination_type=self.params["recombination_type"],
            crossover_type=self.params["crossover_type"],
            mutation_type=self.params["mutation_type"],
            plotting=self.params["plotting"],
        )

        pop.evolve(EA=self.params["training_algorithm"], ea_parameters=self.ea_params)

        non_dom_front = pop.non_dominated()
        self.subnets, self.fitness = self.select(
            pop, non_dom_front, self.params["selection"]
        )
        self.non_linear_layer, _ = self.activation(self.subnets)
        self.linear_layer, *_ = self.calculate_linear(self.non_linear_layer)

    def predict(self, decision_variables):
        """Predict using the EvoDN2 model.

        Parameters
        ----------
        decision_variables : pd.DataFrame
            The decision variables used for prediction.

        Returns
        -------
        y : ndarray
            The prediction of the model.

        """
        non_linear_layer = np.empty((decision_variables.shape[0], 0))

        for i, subnet in enumerate(self.subnets):

            in_nodes = np.asarray(decision_variables)[:, self.subsets[i]]

            for layer in subnet:

                out = np.dot(in_nodes, layer[1:, :]) + layer[0]

                in_nodes = self.activate(self.params["activation_func"], out)

            non_linear_layer = np.hstack((non_linear_layer, in_nodes))

        y = np.dot(non_linear_layer, self.linear_layer)

        return y

    def plot(self, prediction, target, name=None):
        """Creates and shows a plot for the model's prediction.

        Parameters
        ----------
        prediction : np.ndarray
            The prediction of the model.
        target : pd.DataFrame
            The target values.
        name : str
            Filename to save the plot as.
        """
        target = np.asarray(target)
        if name is None:
            name = self.name

        trace0 = go.Scatter(x=prediction, y=target, mode="markers")
        trace1 = go.Scatter(x=target, y=target)
        data = [trace0, trace1]
        plotly.offline.plot(
            data,
            filename="Tests/"
            + self.params["training_algorithm"].__name__
            + self.__class__.__name__
            + name
            + "_var"
            + str(self.num_of_variables)
            + "_nodes"
            + str(self.params["num_subnets"])
            + "_"
            + str(self.params["max_layers"])
            + "_"
            + str(self.params["max_nodes"])
            + ".html",
            auto_open=True,
        )

    def create_logfile(self, name=None):
        """Create a log file containing the parameters for training the model and the EA.

        Returns
        -------
        log_file : file
            An external log file.
        """

        if name is None:
            name = self.name

        # Save params to log file
        log_file = open(
            "Tests/"
            + self.params["training_algorithm"].__name__
            + self.__class__.__name__
            + name
            + "_var"
            + str(self.num_of_variables)
            + "_nodes"
            + str(self.params["num_subnets"])
            + "_"
            + str(self.params["max_layers"])
            + "_"
            + str(self.params["max_nodes"])
            + ".log",
            "a",
        )

        for i in self.params:
            print("", i, ":", self.params[i], file=log_file)

        if self.fitness is not None:
            print("fitness: " + str(self.fitness), file=log_file)

        if self.svr is not None:
            print("single variable response: " + str(self.svr), file=log_file)

        return log_file

    def single_variable_response(self, ploton=False):
        """Get the model's response to a single variable.

        Parameters
        ----------
        ploton : bool
            Create and show plot on/off.

        """

        trend = np.loadtxt("trend")
        avg = np.ones((1, self.num_of_variables)) * (np.finfo(float).eps + 1) / 2
        svr = np.empty((0, 2))
        variables = np.ones((len(trend), 1)) * avg

        for i in range(self.num_of_variables):

            variables[:, i] = trend

            out = self.predict(variables)

            if min(out) == max(out):
                out = 0.5 * np.ones(out.size)
            else:
                out = (out - min(out)) / (max(out) - min(out))

            if ploton:
                trace0 = go.Scatter(
                    x=np.arange(len(variables[:, 1])), y=variables[:, i], name="input"
                )
                trace1 = go.Scatter(
                    x=np.arange(len(variables[:, 1])), y=out, name="output"
                )
                data = [trace0, trace1]
                plotly.offline.plot(
                    data, filename="x" + str(i + 1) + "_response.html", auto_open=True
                )

            p = np.diff(out)
            q = np.diff(trend)
            r = np.multiply(p, q)
            r_max = max(r)
            r_min = min(r)
            s = None
            if r_max <= 0 and r_min <= 0:
                s = "inverse"
            elif r_max >= 0 and r_min >= 0:
                s = "direct"
            elif r_max == 0 and r_min == 0:
                s = "nil"
            elif r_min < 0 < r_max:
                s = "mixed"

            svr = np.vstack((svr, ["x" + str(i + 1), s]))
            self.svr = svr
