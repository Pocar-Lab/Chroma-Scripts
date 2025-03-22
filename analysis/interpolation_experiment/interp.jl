using PyCall, QuanticsTCI
begin
    py"""
        import sys
        sys.path.insert(0, "./")
        """

    #run8 = pyimport("2D-sweep")["run_8_reflector"]
    run_tall_4 = pyimport("loick-2D-sweep")["run_4_tall_reflector"]
	
    println("Running reflectors in julia")

    n = collect(range(0.2, 1.2; length=256))
    spec_ratio = collect(range(0.0, 1.0; length=256))

    global cnt = 0
    function f(a, b)
        global cnt += 1
        println(a)
        println(b)
        a = run_tall_4(a, b)
        println("cnt=$cnt")
        return a
    end
    println(cnt)
    qtt, ranks, errors = quanticscrossinterpolate(Float64, f, [n, spec_ratio]; tolerance=1e-5, maxbonddim=10)
end

begin

    function save_matrix_to_file(matrix::Array{T,2}, filename::String) where {T}
        open(filename, "w") do file
            for row in 1:size(matrix, 1)
                println(file, join(matrix[row, :], " "))
            end
        end
    end


    vals = qtt.(collect(1:256), collect(1:256)')
    # Call the function to save the matrix
    save_matrix_to_file(vals, "matrix_4_tall_n_0.2-1.2_sr_0-1.txt")

end
