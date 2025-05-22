import numpy as np

def numerical_gradient(func, point, step_size=1e-4, method='four'):

    x, y = point
    if method == 'four':
        df_dx = (func((x + step_size, y)) - func((x - step_size, y))) / (2 * step_size)
        df_dy = (func((x, y + step_size)) - func((x, y - step_size))) / (2 * step_size)
    elif method == 'eight':
        df_dx = (
            func((x + step_size, y)) - func((x - step_size, y)) +
            0.5 * (func((x + step_size, y + step_size)) - func((x - step_size, y + step_size))) +
            0.5 * (func((x + step_size, y - step_size)) - func((x - step_size, y - step_size)))
        ) / (3 * step_size)
        df_dy = (
            func((x, y + step_size)) - func((x, y - step_size)) +
            0.5 * (func((x + step_size, y + step_size)) - func((x + step_size, y - step_size))) +
            0.5 * (func((x - step_size, y + step_size)) - func((x - step_size, y - step_size)))
        ) / (3 * step_size)
    else:
        raise ValueError("Invalid method. Choose 'four' or 'eight'.")
    
    return np.array([df_dx, df_dy])

def gradient_descent(func, init_point, learning_rate=0.01, tol=1e-6, max_iters=1000, step_size=1e-4, method='four'):
    
    points = []
    point = np.array(init_point, dtype=float)
    points.append(tuple(point))

    for i in range(max_iters):
        print("Evaluating Gradient Descent at Point (" + str(point[0]) + "," + str(point[1]) + ")")

        grad = numerical_gradient(func, point, step_size, method)
        print("Gradient = " + str(grad[0]) +"," +str(grad[1]))
        new_point = point - learning_rate * grad
        points.append(tuple(new_point))

        print(np.linalg.norm(new_point - point))
        if np.linalg.norm(new_point - point) < tol:
            break
        
        point = new_point
    
    return points
