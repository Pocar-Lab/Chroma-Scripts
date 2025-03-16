using PyCall, QuanticsTCI
begin
    py"""
        import sys
        sys.path.insert(0, "./")
        """

    # run4 = pyimport("2D-sweep")["run_4_reflector"]
    # runLED = pyimport("2D-sweep")["run_LED_reflector"]
    run4shortSilicon = pyimport("2D-sweep")["run_4_short_reflector"]

    #def run_4_short_reflector(k_si, spec_r):


    println("Running reflectors in julia")
    k = collect(range(0.1, 3; length=1024))
    spec_ratio = collect(range(0.1, 1.0; length=1024))
    # spec_ratio = collect(range(0.1, 1.0; length=1024))

    global cnt = 0
    function f(a, b)
        global cnt += 1
        println(a)
        println(b)

        pte = run4shortSilicon(a, b)
        println("cnt=$cnt")
        return pte
    end
    println(cnt)
    qtt, ranks, errors = quanticscrossinterpolate(Float64, f, [k, spec_ratio]; tolerance=1e-4, maxbonddim=10)
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
    save_matrix_to_file(vals, "matrix_4_silicon_short_k_sr.txt")
    exit()

end