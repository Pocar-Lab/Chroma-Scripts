using PyCall, QuanticsTCI
begin
    py"""
        import sys
        sys.path.insert(0, "./")
        """

    #run8 = pyimport("2D-sweep")["run_8_reflector"]
    run_blocked_4 = pyimport("2D-sweep")["run_blocked_half_reflectors"]
	
    println("Running reflectors in julia")
    n = collect(range(0.5, 1.5; length=1024))

    k = collect(range(0.5, 2.5; length=1024))
    # spec_ratio = collect(range(0.1, 1.0; length=1024))

    run_blocked_4(0.1, 0.1, 0.1, 5)
    global cnt = 0
    function f(a, b)
        global cnt += 1
        println(a)
        println(b)
        a = run_blocked_4(a, b, 0.7, 0)[1]
        println("cnt=$cnt")
        return a
    end
    println(cnt)
    qtt, ranks, errors = quanticscrossinterpolate(Float64, f, [n, k]; tolerance=1e-4, maxbonddim=10)
end

begin

    function save_matrix_to_file(matrix::Array{T,2}, filename::String) where {T}
        open(filename, "w") do file
            for row in 1:size(matrix, 1)
                println(file, join(matrix[row, :], " "))
            end
        end
    end


    vals = qtt.(collect(1:1024), collect(1:1024)')
    # Call the function to save the matrix
    save_matrix_to_file(vals, "matrix_half_n_k_scattering_300.txt")

end
