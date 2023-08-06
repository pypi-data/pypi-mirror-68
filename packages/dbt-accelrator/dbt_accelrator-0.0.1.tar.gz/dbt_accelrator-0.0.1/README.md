# dbt_schema_md_generator
This code automatically produces schema.yml and columns.md file with input from xlsx file.


Please follow the Steps below:
1. Input the program with your xlsx filename and model_name_to_append
2. Each Sheet Name will represent a Table and contains the Column_Name, Column_Description and tests if any.
3. Each sheet must contain 'Column_Name' and 'Column_Description' as Headers in them 
4. If you want to add Test you need to add 'Yes' respectively under the test column.
5. Make Sure you have a Table_Descriptions Sheet present in your xlsx file
6. Ensure you have entries for all the Tables in Table_Descriptions Sheet
7. The Sheet Name must match with the Column_Name given in the Table_Descriptions Sheet
8. Please refer to the Sample_File provided for more clarity.