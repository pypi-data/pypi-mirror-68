import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


class Binomial(Distribution):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials

    """

    def __init__(self, prob=.5, size=20):

        Distribution.__init__(self)
        self.p = prob
        self.n = size

    def calculate_mean(self):
        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set

        """

        mean = (self.n)*(self.p)
        self.mean = mean
        return self.mean

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """

        stdev = math.sqrt((self.n)*(self.p)*(1-self.p))
        self.stdev = stdev
        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set

        Args:
            None

        Returns:
            float: the p value
            float: the n value

        """
        self.n = len(self.data)
        self.p = ((self.data).count(1))/(self.n)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """
        x = ['0', '1']
        y = [(self.data).count(0), (self.data).count(1)]
        plt.bar(x, y)
        plt.xlabel('Outcomes')
        plt.ylabel('Count')
        plt.title('Binomial distribution chart')
        # TODO: Use the matplotlib package to plot a bar chart of the data
        #       The x-axis should have the value zero or one
        #       The y-axis should have the count of results for each case
        #
        #       For example, say you have a coin where heads = 1 and tails = 0.
        #       If you flipped a coin 35 times, and the coin landed on
        #       heads 20 times and tails 15 times, the bar chart would have two bars:
        #       0 on the x-axis and 15 on the y-axis
        #       1 on the x-axis and 20 on the y-axis

        #       Make sure to label the chart with a title, x-axis label and y-axis label

    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.

        Args:
            k (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """

        # TODO: Calculate the probability density function for a binomial distribution
        #  For a binomial distribution with n trials and probability p,
        #  the probability density function calculates the likelihood of getting
        #   k positive outcomes.
        #
        #   For example, if you flip a coin n = 60 times, with p = .5,
        #   what's the likelihood that the coin lands on heads 40 out of 60 times?

        first_part = (math.factorial(self.n)/(math.factorial(k) * math.factorial(self.n - k)))
        second_part = ((self.p) ** k)*((1-self.p)**(self.n - k))
        pdf = first_part * second_part
        return pdf

    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """

        # TODO: Use a bar chart to plot the probability density function from
        # k = 0 to k = n

        #   Hint: You'll need to use the pdf() method defined above to calculate the
        #   density function for every value of k.

        #   Be sure to label the bar chart with a title, x label and y label

        #   This method should also return the x and y values used to make the chart
        #   The x and y values should be stored in separate lists

        x = []
        y = []

        # calculate the x values to visualize
        for i in range(self.n):
            x.append(i)
            y.append(self.pdf(i))
        plt.bar(x, y)
        plt.xlabel('Count')
        plt.ylabel('Pdf')
        plt.title('Binomial distribution chart')
        return x, y

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """

        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        result.mean = (result.p)*(result.n)
        result.stdev = math.sqrt(result.n * result.p * (1 - result.p))

        return result

        # TODO: Define addition for two binomial distributions. Assume that the
        # p values of the two distributions are the same. The formula for
        # summing two binomial distributions with different p values is more complicated,
        # so you are only expected to implement the case for two distributions with equal p.

        # the try, except statement above will raise an exception if the p values are not equal

        # Hint: You need to instantiate a new binomial object with the correct n, p,
        #   mean and standard deviation values. The __add__ method should return this
        #   new binomial object.

        #   When adding two binomial distributions, the p value remains the same
        #   The new n value is the sum of the n values of the two distributions.

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Gaussian

        """
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
