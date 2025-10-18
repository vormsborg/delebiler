from dataclasses import dataclass



#%% DATA CLASSES

@dataclass
class KintoModel:
    """
    Data Class to store the data and make calculations for a car following the kinto model.
    """

    model        : str
    pris_pr_time : int
    pris_pr_dgn  : int
    pris_pr_uge  : int
    pris_pr_km   : float

    def calculate_price_per_distance(self, km) -> float:
        """
        Calculates the price for the distance portion
        """

        price = self.pris_pr_km*km

        return price

    def calculate_price_hourly(self, hours):

        price = self.pris_pr_time*hours

        return price
    
    def calculate_price_daily(self, days):
        
        price = self.pris_pr_dgn*days
        return price
    
    def calculate_price_weekly(self, weeks):
        
        price = self.pris_pr_uge*weeks
        return price

    def calculate_total_price(self, hours, days, weeks, km) -> float:
        """
        Calculates the total price by summing
            pricing for the distance
            pricing for hours
            pricing for days
            pricing for weeks
        """

        total_price = sum([
            self.calculate_price_per_distance(km),
            self.calculate_price_hourly(hours),
            self.calculate_price_daily(days),
            self.calculate_price_weekly(weeks),
        ])
        
        return total_price

@dataclass
class HyreModel:
    """
    Data Class to store the data and make calculations for a car following the Hyre model.
    """

    model        : str
    pris_pr_time : int
    pris_pr_dgn  : int
    pris_pr_uge  : int
    pris_pr_km   : float
    pris_pr_braendstof_pr_km : float
    gratis_km_pr_dgn : int

    def calculate_price_per_distance(self, km) -> float:
        """
        Calculates the price for the distance portion
        """

        price = self.pris_pr_km*km

        return self.pris_pr_braendstof_pr_km*km

    def calculate_price_fuel_per_distance(self, km):

        price = self.pris_pr_braendstof_pr_km*km
        return price

    def calculate_price_hourly(self, hours):

        price = self.pris_pr_time*hours

        return price
    
    def calculate_price_daily(self, days):
        
        price = self.pris_pr_dgn*days
        return price
    
    def calculate_price_weekly(self, weeks):
        
        price = self.pris_pr_uge*weeks
        return price

    def calculate_total_days(self, days, weeks):

        total_days = sum([
            1,
            days,
            weeks*7
        ])

        return total_days
    
    def calculate_total_km_discount(self, days, weeks, km):

        ## Calculate total days
        total_days = self.calculate_total_days(
            days, weeks
        )

        ## Calculate km discount for total days
        km_discount = total_days*self.gratis_km_pr_dgn

        ## Subtract km_discount from total km
        km_actual   = km - km_discount

        ## Make sure km actual is not negative
        if km_actual < 0:
            km_actual = 0

        return km_actual

    def calculate_total_price(self, hours, days, weeks, km):

        km_actual = self.calculate_total_km_discount(days, weeks, km)
        total_price = sum([
            self.calculate_price_per_distance(km_actual),
            self.calculate_price_fuel_per_distance(km),
            self.calculate_price_hourly(hours),
            self.calculate_price_daily(days),
            self.calculate_price_weekly(weeks),
        ])

        return total_price

@dataclass
class LetsgoModel:

    model        : str
    pris_pr_time : int
    pris_pr_dgn  : int
    pris_pr_uge  : int
    pris_pr_km   : float
    bestillingsgebyr : float

    def calculate_total_price(self, hours, days, weeks, km):


        admission_fee = self.bestillingsgebyr

        price_for_hours = hours  *  self.pris_pr_time
        price_for_days  = days   *  self.pris_pr_dgn
        price_for_weeks = weeks  *  self.pris_pr_uge
        price_for_km    = km     *  self.pris_pr_km

        total_price = sum([
            admission_fee,
            price_for_hours,
            price_for_days,
            price_for_weeks,
            price_for_km
        ])

        return total_price

@dataclass
class NordsjaellandsDelebilerModel:

    model                       : str
    pris_pr_time                : int
    pris_pr_km                  : float
    pris_pr_time_efter_12_timer : float
    pris_pr_km_efter_100_km     : float

    def calculate_total_price(self,  hours, days, weeks, km):

        # calculate_total_hours
        total_hours = hours + (days*24) + (weeks*24*7)

        # caculate_price for hours
        if not total_hours > 12:
            price_for_hours = total_hours * self.pris_pr_time
        else:
            price_for_hours = sum([
                12 * self.pris_pr_time,
                (total_hours-12) * self.pris_pr_time_efter_12_timer
            ])

        # calculate price for distance
        if not km > 100:
            price_for_km = km * self.pris_pr_km
        else:
            price_for_km = sum([
                100 * self.pris_pr_km,
                (km-100) * self.pris_pr_km_efter_100_km
            ])

        total_price = sum([price_for_hours, price_for_km])

        return total_price

@dataclass
class TotalPrice:
    """
    Dataclass to store the total price
    """
    company     : str
    car_model   : str
    total_price : int
