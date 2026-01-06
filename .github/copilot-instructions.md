# BAC Object Registration Automation Instructions

## CRITICAL EXECUTION RULES
1. **NO HALLUCINATIONS**: Only use information from `object.json` and MD template files
2. **NO ASSUMPTIONS**: If information is missing, ask the user explicitly
3. **NO SKIPPING**: Read complete files without line limits
4. **NO BACKUPS**: Do not create backup files unless explicitly requested
5. **STRICT VALIDATION**: Verify each step completion before proceeding to next step
6. **EXACT PATHS**: Use the configured paths exactly as defined below
7. **NAME CONVENTIONS**: Follow naming conventions strictly as per templates and it should be consistent across all files and CollectionCategory naming should be just CASE-SENSITIVE object template name
8. **DRY RUN DEFAULT**: All MCP tool invocations should default to `dry_run=true` unless specified otherwise
9. **USE `wsl -d WindchillVM` after step 12**: to run commands in WindchillVM WSL before that do not use this
---

## PATH CONFIGURATION (DO NOT MODIFY)
```
wt_path              = \\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\wt\
test_path            = \\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src_test\wt\
object_json_path     = c:\FINAL\.github\object.json
bac_src_path         = \\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\
ixl_handler_path     = \\wsl.localhost\WindchillVM\opt\wnc\Windchill\DevModules\IXLoad\src\wt\ixb\handlers\forclasses\
obj_registry_path    = \\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\com\ptc\windchill\bac\objreg\
service_xconf_path   = \\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\com\ptc\windchill\bac\BAC-service.properties.xconf
md_templates_path    = C:\FINAL\md\
test_templates_path   = C:\FINAL\test\
preview = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/client/delegates/preview/impl/`
preview_delegate_path = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/client/`

```

---

## TO BE NOTED
- CollectionCategory naming should be just CASE-SENSITIVE object template name
- Use `wsl -d WindchillVM -- <command>` after 12 steps to run commands in WindchillVM WSL
## WORKFLOW EXECUTION SEQUENCE

### STEP 1: Object Selection & Initialization
**ACTION**: 
- Read `object.json` from `object_json_path` completely (no line limits)
- Display all available objects to user
- Ask user: "Which object would you like to work with?"
- Store user's selection in variable `selected_object`
- Extract all properties for `selected_object`:
  - `template`
  - `directory` 
  - `key_attributes`
  - `dependencies`

**VALIDATION**: Confirm all object properties are extracted before proceeding

---

### STEP 2: Directory Structure Creation
**ACTION**:
- Determine directory name from `selected_object.directory` or use object name if directory not specified
- Create folder structure: `{wt_path}{directory_name}\bac\`
 - Use MCP Tool: `ensure_directories`
   - Parameters: `directory_name = <domain dir like wt.change2>`
   - as after `wt.change2` in this path change2 is directory name
   - Outcome: Creates both `{wt_path}{directory_name}\bac\` and `{test_path}{directory_name}\bac\`

Tool Invocation Example:
```
ensure_directories(directory_name="change2")
```

**VALIDATION**: Verify directory creation successful before proceeding

---

### STEP 3: Register Admin Object

## MCP Tool Usage
- Use MCP Tool: `register_admin_object`
  - Required params: `template`, `registry_file`
  - Optional: `properties` (extra attributes), `dry_run` (default `true`)
  - Behavior: Appends a new entry to the target registry XML, validates XML syntax, and does not modify existing entries.

Tool Invocation Example:
```
register_admin_object(
  template="WTChangeOrder2",
  registry_file="\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\com\\ptc\\windchill\\bac\\objreg\\obj_registry.xml",
  properties={"owner":"BAC"},
  dry_run=true
)
```

**VALIDATION**: 
- Confirm XML syntax is valid
- Confirm new entry added
- DO NOT modify existing entries

---

### STEP 4: Register Collection Category

## MCP Tool Usage
- Use MCP Tool: `register_collection_category`
  - Required params: `source_file` (path to `CollectionCategory.java`), `template_name` (CASE-SENSITIVE)
  - Optional: `dry_run` (default `true`)
  - Behavior: Inserts `public static final CollectionCategory <Template> = toCollectionCategory("<Template>");` after the last constant anchor.

Tool Invocation Example:
```
register_collection_category(
  source_file="\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\com\\ptc\\windchill\\bac\\CollectionCategory.java",
  template_name="WTChangeOrder2",
  dry_run=true
)
```

**VALIDATION**: Confirm category registration complete

---

### STEP 5: Generate Delegate Files

- Collection Category naming should be just CASE-SENSITIVE object template name 

**INSTRUCTION FILES**: 
- Collection Delegate --> `collection.md`
- DeleteRecord Delegate --> `deleterecord.md`
- DeleteRecordAttr Delegate --> `deleterecordattr.md`
- Identity Delegate --> `identity.md`
- Processor Delegate --> `processor.md`
- Report Delegate --> `report.md`
- SpecProcessor Delegate --> `spec.md`
- Tracking Delegate --> `tracking.md`

**ACTION FOR EACH FILE**:
1. Read complete MD file from `{md_templates_path}` (no line limits)
2. Generate Java delegate file following template instructions
3. Replace all placeholders with actual values from `selected_object`
4. Save generated file to: `{wt_path}{directory_name}\bac\{DelegateName}.java`
5. Ensure proper Java syntax and package declarations

**VALIDATION**: 
- Verify 7 delegate files created
- Confirm each file has valid Java syntax
- Confirm proper package naming: `wt.{directory_name}.bac`

---

### STEP 6: Generate ExpImp Handler
**INSTRUCTION FILE**: `{md_templates_path}expimp.md`

**ACTION**:
- Read complete `expimp.md` file (no line limits)
- Generate handler Java file following template
- Save to: `{ixl_handler_path}{selected_object.template}Handler.java`
- Ensure proper imports and class structure

**VALIDATION**: Confirm handler file created with valid Java syntax

---

### STEP 7: Register Services
- `service_path` = `\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\com\\ptc\\windchill\\bac\\BAC-service.properties.xconf`
- `delegate_folder` = `\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\wt\\{object_directory}\\bac\\`

## MCP Tool Usage
- Use MCP Tool: `register_services`
  - Required params: `delegate_folder`, `selector`
  - Optional: `service_xconf` (defaults to configured `service_xconf_path`), `dry_run` (default `true`)
  - Behavior: Scans `.java` classes in `delegate_folder`, matches known service types, and adds missing `<Option>` entries to `BAC-service.properties.xconf` using the provided `selector`.

Tool Invocation Example:
```
register_services(
  delegate_folder="\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\wt\\change2\\bac\\",
  selector="WTChangeOrder2",
  service_xconf="\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\com\\ptc\\windchill\\bac\\BAC-service.properties.xconf",
  dry_run=true
)
```

## Validation Steps
1. **First**: After adding the new service registration, validate the `BAC-service.properties.xconf` file for correct XML syntax
2. **Second**: Ensure that the new service registration follows the existing pattern and conventions
3. **Third**: Each delegate from `delegate_folder` should have a corresponding service registration entry in `BAC-service.properties.xconf`

**VALIDATION**:
- Confirm all 7 delegates registered
- Validate XML syntax
- DO NOT modify existing service entries

---

### STEP 8: Update BAC Specifications

## MCP Tool Usage
- Use MCP Tool: `update_bac_spec`
  - Required params: `template_name`
  - Optional: `attributes` (list of attribute names), `bacspec_xsd_path` (defaults to configured schema path), `dry_run` (default `true`)
  - Behavior: Adds both `<xs:complexType name="Template">` and `<xs:element name="Template" type="bac:Template">` entries to `BACSpec.xsd`

Tool Invocation Example:
```
update_bac_spec(
  template_name="WTChangeOrder2",
  attributes=["status", "priority"],
  bacspec_xsd_path="\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\com\\ptc\\windchill\\bac\\schema\\BACSpec.xsd",
  dry_run=true
)
```

**VALIDATION**: Confirm spec entry added correctly

---

### STEP 9: Update Delete Records

## MCP Tool Usage
- Use MCP Tool: `update_bac_generic_delete`
  - Required params: `template_name`
  - Optional: `generic_xsd_path` (defaults to configured schema path), `dry_run` (default `true`)
  - Behavior: Adds `<xs:element name="Template" type="xs:string">` entry to `BACGenericDeleteRecordObjInfos.xsd`

Tool Invocation Example:
```
update_bac_generic_delete(
  template_name="WTChangeOrder2",
  generic_xsd_path="\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\com\\ptc\\windchill\\bac\\schema\\BACGenericDeleteRecordObjInfos.xsd",
  dry_run=true
)
```

**VALIDATION**: Confirm delete record entry added

---

### STEP 10: Update RB Info

## Directory Configuration
- `category_path` = `\\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\com\ptc\windchill\bac\`

## Category Registration Process
- Get `CollectionCategoryRB.rbInfo` file from `category_path`
- Understand the structure of `CollectionCategoryRB.rbInfo` file
- Based on the object information from `object.json`, identify the categories to be registered
- Register the same Template name which is used above in chat
- For each category to be registered, create a new entry in `CollectionCategoryRB.rbInfo` file
- Follow the existing pattern for category registration

---

### STEP 11: Batch Preview

**INSTRUCTION FILE**: `{md_templates_path}preview.md`

**ACTION**:
- Read `preview.md` which contains instructions to create a `BatchPreviewDelegate` implementation.
- Use `preview.md` to generate a `Batch[ObjectName]PreviewDelegate.java` (BatchPreviewDelegate) following the guidance in that file.
- Suggested sections in `preview.md` for the human-readable batch preview summary:
  - Summary: object name and template
  - Files created: bullet list with full paths
  - Registry entries added: brief descriptions and locations
  - Warnings/Errors: any issues encountered during generation
- then read a `BAC-delegates.xconf` file from `preview_delegate_path` to register the generated delegate.
- understand the structure of `BAC-delegates.xconf` file
- Add a new entry for the generated `BatchPreviewDelegate` in `BAC-delegates.xconf` file following the existing pattern.
- and ensure proper package declaration and imports in the generated Java file. 

**OUTPUT LOCATION**:
- The generated `BatchPreviewDelegate` (if created) should be saved to the delegate output folder noted in `preview.md` (default: `.github/generated_delegates/`) or to `{preview}` if configured that way.

**VALIDATION**: Confirm `preview.md` exists and contains the sections above
 
<!-- ### STEP 11.1: Register Preview

**PURPOSE**: Ensure the generated batch preview delegate is registered and discoverable by the preview subsystem.

**ACTION**:
- Determine the preview delegate class name (recommended: `Batch<Template>PreviewDelegate`) using the selected object `template`.
- Add a registration entry for the preview delegate in the preview delegate registry or the configured preview delegate folder index. If the project uses a central preview registry file, append the appropriate entry following existing patterns.
- If the project exposes a preview delegate package or config under the `preview` path (see preview variable in PATH CONFIGURATION), ensure the generated delegate is placed or referenced there.

**VALIDATION**:
- Confirm an entry or reference for `Batch<Template>PreviewDelegate` was added to the preview registry or index.
- Confirm the preview delegate Java file exists at the expected location and uses the correct package `wt.{directory_name}.bac`.
- If the preview system requires a service registration in `BAC-service.properties.xconf`, ensure the corresponding `<Option>` is present (use `register_preview_delegate` to validate). -->

### STEP 12: Delta Controller

**INSTRUCTION FILE**: `{md_templates_path}deltacontroller.md`

**VALIDATION**:
- Confirm the DeltaController file is updated in the controllers directory
- Verify Java syntax for the modified file (or request build logs if compilation is required)

---

### STEP 12.1: Register Export Helper

## MCP Tool Usage
- Use MCP Tool: `register_export_helper`
  - Required params: `template_name`
  - Optional: `export_helper_path` (defaults to configured path), `dry_run` (default `true`)
  - Behavior: Adds a new object type entry to `BACExportHelper.java` `typesXmlSpec` method

Tool Invocation Example:
```
register_export_helper(
  template_name="WTChangeOrder2",
  export_helper_path="\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\com\\ptc\\windchill\\bac\\BACExportHelper.java",
  dry_run=true
)
```

**VALIDATION**: 
- Confirm export helper entry added correctly
- Verify Java syntax is valid
- DO NOT modify existing entries

---

### STEP 13: Test Generation
**INSTRUCTION FILE**: 
CollectionTest --> `{test_templates_path}collectionTest.md`
DeleteRecordTest --> `{test_templates_path}deleterecordTest.md`
DeleteRecordAttrTest --> `{test_templates_path}deleterecordattrTest.md`
IdentityTest --> `{test_templates_path}identityTest.md`
ProcessorTest --> `{test_templates_path}processorTest.md`
ReportTest --> `{test_templates_path}reportTest.md`
SpecProcessorTest --> `{test_templates_path}specprocessorTest.md`
TrackingTest --> `{test_templates_path}trackingTest.md`

**ACTION**:
**ACTION FOR EACH FILE**:
1. Read complete MD file from `{test_templates_path}` (no line limits)
2. Generate Java delegate file following template instructions
3. Replace all placeholders with actual values from `selected_object`
4. Save generated file to: `{test_path}{directory_name}\bac\{DelegateTestName}.java`
5. Ensure proper Java syntax and package declarations

**VALIDATION**: 
- Verify 7 delegateTest files created
- Confirm each file has valid Java syntax
- Confirm proper package naming: `wt.{directory_name}.bac`

---



## COMPLETION CHECKLIST
After completing all steps, verify:
- [ ] Admin object registered in `obj_registry.xml`
- [ ] Collection category registered
- [ ] 7 delegate files generated in `{wt_path}{directory_name}\bac\`
- [ ] ExpImp handler generated in `{ixl_handler_path}`
- [ ] All delegates registered in `BAC-service.properties.xconf`
- [ ] BAC specifications updated
- [ ] Delete records updated
- [ ] RB info updated
- [ ] (If applicable) BatchPreviewDelegate generated and saved
- [ ] (If applicable) DeltaController updated/created
- [ ] 7 test delegate files generated in `{test_path}{directory_name}\bac\`
- [ ] All validations for each step confirmed

**FINAL ACTION**: Report completion status to user with summary of all files created/modified

---

## ERROR HANDLING
- If any step fails, STOP and report error to user
- If information is missing from `object.json`, ASK user for clarification
- If MD template is unclear, ASK user for guidance
- DO NOT proceed with assumptions or placeholder values
- DO NOT hallucinate file contents or configurations

---

## FINAL BUILD & ENVIRONMENT STEPS
After all registration and file-generation steps are completed and validated, perform the following environment and build steps to compile the BAC sources.

1. **Set Windchill build environment (inside WindchillVM WSL)**:
  - Run it inside the `WindchillVM` WSL distribution (non-interactive example):

```
wsl -d WindchillVM
```

2. Set Windchill environment :

```
wnc_env urel_241
```

3. After Setting the environment, navigate to the BAC module directory:

```
cd /opt/wnc/wcmod/modules/BAC/src
```

4. **Compile BAC module using Ant**:
  - Execute the Ant build command to compile the BAC sources:

```
ant clean clobber all
```

5. **Post-Build Validation**:

``` 
start_windchill
```

- Every command in this should be seperate and new command block as every previous command should be completed before next command is run.

---

## STEP 14: Execute BAC SQL Scripts

**PURPOSE**: After a successful build, execute the required SQL scripts to set up database objects and configurations for the registered BAC object.

**SQL SCRIPTS LOCATION**: 
```
sql_scripts_path = \\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\db\sql3\
```

**ACTION**:
1. **Identify SQL Script Files**:
   - Based on the `selected_object` and its template name
   - Locate corresponding SQL scripts in `{sql_scripts_path}` directory
   - Common SQL script patterns:
     - `create_<object_name>_tables.sql` - Creates database tables
     - `insert_<object_name>_metadata.sql` - Inserts metadata records
     - `grant_<object_name>_permissions.sql` - Grants necessary permissions
     - `create_<object_name>_indexes.sql` - Creates database indexes

2. **Database Connection Configuration**:
   - Retrieve database connection details from Windchill configuration:
     - Host: From `wt.properties` or environment variables
     - Port: Default Oracle port (1521) or configured port
     - Service Name/SID: From Windchill database configuration
     - Username: Windchill database user (typically from `wt.properties`)
     - Password: Windchill database password (secure retrieval)

3. **Execute SQL Scripts**:
   - Use `wsl -d WindchillVM` to execute SQL scripts within the WindchillVM environment
   - Execute scripts in the correct order:
     1. Table creation scripts first
     2. Metadata insertion scripts second
     3. Index creation scripts third
     4. Permission grants last
   
   Example execution command pattern:
   ```bash
   wsl -d WindchillVM -- bash -c "source /opt/wnc/wnc_env urel_241 && sqlplus <username>/<password>@<host>:<port>/<service> @/opt/wnc/wcmod/modules/BAC/db/sql3/<script_name>.sql"
   ```

4. **Script Execution Validation**:
   - Verify each script executes successfully (exit code 0)
   - Check for SQL errors in output
   - Validate that expected database objects were created:
     - Query database to confirm tables exist
     - Verify metadata records were inserted
     - Confirm indexes were created

5. **Error Handling**:
   - If script execution fails, capture error message
   - Log failed script name and error details
   - STOP execution and report to user
   - Provide rollback guidance if needed

**VALIDATION CHECKLIST**:
- [ ] SQL scripts identified for selected object
- [ ] Database connection parameters retrieved
- [ ] Scripts executed in correct order
- [ ] All scripts completed without errors
- [ ] Database objects verified to exist
- [ ] Metadata records confirmed in database
- [ ] Indexes created successfully

**EXAMPLE EXECUTION**:
For a `WTChangeOrder2` object:
```bash
# Step 1: Navigate to SQL directory
wsl -d WindchillVM -- bash -c "cd /opt/wnc/wcmod/modules/BAC/db/sql3"

# Step 2: Execute table creation
wsl -d WindchillVM -- bash -c "source /opt/wnc/wnc_env urel_241 && sqlplus wcadmin/password@localhost:1521/windchill @create_wtchangeorder2_tables.sql"

# Step 3: Execute metadata insertion
wsl -d WindchillVM -- bash -c "source /opt/wnc/wnc_env urel_241 && sqlplus wcadmin/password@localhost:1521/windchill @insert_wtchangeorder2_metadata.sql"

# Step 4: Verify database objects
wsl -d WindchillVM -- bash -c "source /opt/wnc/wnc_env urel_241 && sqlplus -s wcadmin/password@localhost:1521/windchill <<< 'SELECT table_name FROM user_tables WHERE table_name LIKE \"%WTCHANGEORDER2%\";'"
```

**POST-EXECUTION**:
- Restart Windchill services to ensure changes are loaded:
```bash
wsl -d WindchillVM -- bash -c "source /opt/wnc/wnc_env urel_241 && windchill stop && windchill start"
```

**NOTES**:
- SQL scripts may need to be generated based on object template if not pre-existing
- Database credentials should be handled securely (environment variables or secure vault)
- Each SQL script execution should be logged for audit purposes
- Consider transaction rollback capabilities for failed executions
