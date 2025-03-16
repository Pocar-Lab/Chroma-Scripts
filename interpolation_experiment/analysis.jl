using Plots
# Function to load matrix from a text file
function load_matrix_from_file(filename::String)
    matrix = []
    open(filename, "r") do file
        for line in eachline(file)
            # Split the line by spaces and convert to Float64
            row = parse.(Float64, split(line, " "))
            push!(matrix, row)
        end
    end
    return hcat(matrix...)'  # Convert the array of rows into a matrix
end


# 8 reflectors
begin
    println("Calculating score for 8 reflectors")
    filename = "short-8-silicon-sweep.txt"
    loaded_matrix8 = load_matrix_from_file(filename)
    θ8 = 21 # degrees TODO 

    no_reflector8 = .0013 #no reflector PTE TODO
    PTE_ratio8 = loaded_matrix8./no_reflector8

    #alpha ratio 
    A8 = 2.1 #TODO 
    
    score8 = - abs.(PTE_ratio8 .- A8)

end

# 4 reflectors
begin
    println("Calculating score for 4 reflectors")

    filename = "matrix_4_k_sr.txt"
    loaded_matrix4 = load_matrix_from_file(filename)
    θ4 =45 # degrees TODO 

    no_reflector4 = 0.001268 #no reflector PTE TODO
    PTE_ratio4 = loaded_matrix4./no_reflector4

    #alpha ratio 
    A4 = 1.8 #TODO 
    
    score4 = -abs.(PTE_ratio4 .- A4)

end

# half reflectors
begin
    println("Calculating score for half reflectors")

    filename = "matrix_half_k_sr.txt"
    loaded_matrix_half = load_matrix_from_file(filename)
    θ_half =65 # degrees TODO 

    no_reflector_half = 0.003568 #no reflector PTE TODO
    PTE_ratio_half = loaded_matrix_half./no_reflector_half

    #alpha ratio 
    A_half = 1.0 #TODO 
    
    score_half = -abs.(PTE_ratio_half .- A_half)
    combinedScore = score4 + score_half

end


begin
    println("Calculating score for LED reflectors")

    filename = "matrix_LED_k_sr.txt"
    loaded_matrix_led = load_matrix_from_file(filename)
    θ_led =65 # degrees TODO 

    no_reflector_led = 0.00168 #no reflector PTE TODO
    PTE_ratio_led = loaded_matrix_led./no_reflector_led

    #alpha ratio 
    A_led = 1.9 #TODO 
    
    score_led = -abs.(PTE_ratio_led .- A_led)
    combinedScore = score4 + score_led

end


begin
    println("Calculating score for tilted reflectors")

    filename = "matrix_tilted_k_sr.txt"
    loaded_matrix_tilt = load_matrix_from_file(filename)
    θ_tilt =65 # degrees TODO 

    no_reflector_tilt = 0.001168 #no reflector PTE TODO
    PTE_ratio_tilt = loaded_matrix_tilt./no_reflector_tilt

    #alpha ratio 
    A_tilt = .9 #TODO 
    
    score_tilt = -abs.(PTE_ratio_tilt .- A_tilt)
    combinedScore = score_half + score_tilt
    # heatmap(k, spec_ratio, score_tilt)

end


begin 


end


begin   
    using Plots
    k = collect(range(0.1, 3; length=1024))
    spec_ratio = collect(range(0.1, 1.0; length=1024))
    # c = cgrad([:red,:blue,:purple, :white], [0.000,  0.5, 0.8, .999], categorical = false)

    h1 = heatmap(k, spec_ratio, score4)
    title!("4 Reflectors")
    h2 = heatmap(k, spec_ratio, score8)
    title!("8 Reflectors")

    h3 = heatmap(k, spec_ratio, score_half)
    title!("half Reflectors")

    h4 = heatmap(k, spec_ratio, score_led)
    title!("LED Frequency Reflectors")

    h5 = heatmap(k, spec_ratio, score_tilt)
    title!("Tilted Reflectors")


    



    h6 = heatmap(k, spec_ratio, combinedScore)
    # plot(h1, h2, layout=(1, 2))
    p1 = plot(h1, h2, h3,h4,h5, layout=(2, 3), size= (1200, 600))

    # plot(p1, h5, layout=(2, 1), size=(900, 900))


end


begin
    k = collect(range(0.1, 3; length=1024))
    gamma = collect(range(0.1, 1.0; length=1024))

    # Plot the heatmaps with contours for score = 0
    heatmap1 = heatmap(k, gamma, score4, c=:viridis, title="4 Reflectors")
    c1 = contour!(k, gamma, score4, levels=[-.01], c=:red, linewidth=2)

    heatmap2 = heatmap(k, gamma, score8, c=:viridis, title="8 Reflectors")
    c2 = contour!(k, gamma, score8, levels=[-.01], c=:red, linewidth=2)

    plot(c1, c2, layout=(1, 2))
end





    
begin
    using Plots
    filename1 = "short-8-silicon-sweep.txt"
    filename2 = "matrix_4_k_sr.txt"


    loaded_matrix = load_matrix_from_file(filename)
    # m = reshape(matrix, (1024, 1024))
    k = collect(range(0.1, 3; length=1024))
    spec_ratio = collect(range(0.1, 1.0; length=1024))
    p1 = heatmap(k, spec_ratio, load_matrix_from_file(filename1))
    xlabel!("k")
    ylabel!("Specular Ratio")
    p2 = heatmap(k, spec_ratio, load_matrix_from_file(filename2))
    heatmap(p1, p2, layout=(1,2 ), size=(2000, 1000))

    title!("k vs γ sweep using Quantics Tensor Cross Interpolation\n 10,000 evaluations -> 1,000,000 grid points\n")
    end
    
    
    begin
        
        using Printf
    
        function Rs(n1, n2, theta_i)
            # Convert theta_i to radians for the trigonometric functions
            theta_i_rad = deg2rad(theta_i)
            
            # Calculate sin(theta_i)
            sin_theta_i = sin(theta_i_rad)
    
            # Calculate cos(theta_i)
            cos_theta_i = cos(theta_i_rad)
    
            # Calculate cos(theta_t) using Snell's Law
            sqrt_term = sqrt(1 - (n1 / n2 * sin_theta_i)^2)
            
            # Calculate the numerator and denominator
            numerator = n1 * cos_theta_i - n2 * sqrt_term
            denominator = n1 * cos_theta_i + n2 * sqrt_term
            
            # Reflectance Rs
            Rs_value = (numerator / denominator)^2
            
            return Rs_value
        end
    
    # Example usage:
    n1 = 1.4  # Index of refraction for medium 1
    n2 = 1.5  # Index of refraction for medium 2
    theta_i = 30.0  # Incident angle in degrees
    
    result = Rs(n1, n2, theta_i)
    @printf("Rs for θ_i = %.2f°: %.6f\n", theta_i, result)
    
    
    result = Rs(n1, n2, theta_i)/Rs(n1, n2, 45)
    println(result)
    
    
    end