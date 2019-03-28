# egt
Code for CVPR2019 paper: Explore-Exploit Graph Traversal for Image Retrieval

Require java 1.8

For executable jar, compile with
`mvn clean compile assembly:single`

Execute jar with
` java -jar target/egt.jar`

For graph generation and evaluation, see python folder.
For research and development on top of EGT, see `src/main/java/EGT.java` on how to execute `EGTImpl` directly.





#####################################################

Example to generate a "prebuild" file from embedding:
    ```cd into python directory and run:
    python egt.py --query_features ../data/roxHD_query_fused_3s_cq.npy --index_features ../data/roxHD_index_fused_3s_cq.npy --query_hashes query_hashes.txt --index_hashes index_hashes.txt --Do_QE False --Num_candidates 300 --OutputFile prebuild_from_python.txt --evaluate roxford5k```


`To generate the egt result from a prebuild file:`
    ```mvn exec:java -Dexec.mainClass="EGT" -Dexec.args="-k 250 -q 70 -t 420000 -p 5000 python/prebuild_from_python.txt test.txt```


`To evaluate a file with one header line:`
    ```python evaluate_prebuild.py --f ../test.txt --index_hashes index_hashes.txt --num_query 70 --num_score 0 --evaluate roxford5k --skip 1```
#####################################################
