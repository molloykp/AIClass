class points_decor:
    points_awarded = 0
    total_possible_points = 0
    scored_functions = {}

    def __init__(self,points,autograder_name=None):
        self.points = points
        self.autograder_name = autograder_name

        points_decor.scored_functions[self.autograder_name] = 0

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            #print('points awarded so far:', points_decor.points_awarded)
            #print('this func (',func.__name__, ') points are:',self.points)
            points_decor.total_possible_points += self.points
            x = None
            try:
                x = func(*args, **kwargs)
                points_decor.points_awarded += self.points
                #print('after total points:', points_decor.points_awarded)
                points_decor.scored_functions[self.autograder_name] += self.points
                return x
            except:
                raise
        return wrapper

    @staticmethod
    def print_json():
        print('\n{"scores": {', end='')
        first = True
        for k, v in points_decor.scored_functions.items():
            if first == False:
                print(', ', end='')
            else:
                first = False

            print('"', k, '":', v, end='', sep='')
        print('}}')

    @staticmethod
    def return_points():
        return points_decor.points_awarded

