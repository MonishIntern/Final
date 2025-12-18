# BAC Object Registration Automation Instructions

## CRITICAL EXECUTION RULES
1. **NO HALLUCINATIONS**: Only use information from `object.json` and MD template files
2. **NO ASSUMPTIONS**: If information is missing, ask the user explicitly
3. **NO SKIPPING**: Read complete files without line limits
4. **NO BACKUPS**: Do not create backup files unless explicitly requested
5. **STRICT VALIDATION**: Verify each step completion before proceeding to next step
6. **EXACT PATHS**: Use the configured paths exactly as defined below
7. **NAME CONVENTIONS**: Follow naming conventions strictly as per templates and it should be consistent across all files and CollectionCategory naming should be just CASE-SENSITIVE object template name

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

preview = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/client/delegates/preview/`

```

---

## TO BE NOTED
- CollectionCategory naming should be just CASE-SENSITIVE object template name

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
- Use PowerShell command: `New-Item -ItemType Directory -Force -Path "{wt_path}{directory_name}\bac"`

**VALIDATION**: Verify directory creation successful before proceeding

---

### STEP 3: Register Admin Object

## Directory Configuration
`obj_path` = `\\\\wsl.localhost\\WindchillVM\\opt\\wnc\\wcmod\\modules\\BAC\\src\\com\\ptc\\windchill\\bac\\objreg\\`

## Directory Access Commands
```bash
# Navigate to target directory
cd {obj_path}

# Show directory structure
ls -la
```

## Object Registration Process
- Understand the structure of object registration files in `obj_path` of `obj_registry.xml`
- Identify the appropriate file for registering a new BAC Admin Object
- Based on the object details provided, create a new registration entry at the end of the appropriate registration file
- add this object as new entry in the appropriate registration file within `obj_path`
- Donot alert any other admin object 

**VALIDATION**: 
- Confirm XML syntax is valid
- Confirm new entry added
- DO NOT modify existing entries

---

### STEP 4: Register Collection Category

## Directory Configuration
- `ba_path` = `\\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\com\ptc\windchill\bac\`

## Directory Access Commands
```bash
# Navigate to target directory
cd {ba_path}
# Show directory structure
ls -la
```
## collection category
- Ask User for Object Name to add Collection Category
- After getting Object Name from user, perform following steps
- Object_name = User Provided Object Name
- navigate to directory:
```bash
find . -name "*CollectionCategory*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```
- understand existing Collection Category patterns
```java
public static final CollectionCategory TEMPLATE = toCollectionCategory("Template");
```
- Add Collection Category for the provided Object Name
- add this object as a new constant in the CollectionCategory enum or class

**VALIDATION**: Confirm category registration complete

---

### STEP 5: Generate Delegate Files
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

## Directory Access Commands
```bash
# Navigate to target directory
cd {delegate_folder}

# Show directory structure
ls -la
```
## Delegate List
- List down all available delegate in delegate_folder
- Make a Note of this delegate

## Service Registration Process
- Understand the structure of `BAC-service.properties.xconf` file from `service_path`
- Identify where to add new service registration
- Traverse thourgh each file in `delegate_folder` and check if all files in this folder are register in `BAC-service.properties.xconf` if not then register with appropriate entry
- Based on the delegate noted earlier, create a new service registration entry
- Follow the existing pattern for service registration

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

## Directory Configuration
`bacspec_path` = `\\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\com\ptc\windchill\bac\schema\`

## BAC Specification Update Process
1. **Navigate to BAC Specification Directory**:
   ```bash
   cd {bacspec_path}
   ```
2. **BACSpec.xsd**:
   - Locate the `BACSpec.xsd` file in the `bacspec_path` directory.
   - This file defines the XML schema for BAC specifications.
3. **Update BACSpec.xsd**:
    - Based on the object information from `object.json`, identify the necessary updates to the BAC specifications.
    - Make the required changes to the `BACSpec.xsd` file, ensuring that all new elements and attributes are correctly defined according to XML schema standards.
    - Do not add any new attributes in object if user havent provided it

## Pattern for BACSpec.xsd Update
- <xs:complexType name="Template">    </xs:complexType>

- <xs:element name="Template" type="bac:Template" minOccurs="0" maxOccurs="1" />

**VALIDATION**: Confirm spec entry added correctly

---

### STEP 9: Update Delete Records

## Directory Configuration
- `generic_path` = `\\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\com\ptc\windchill\bac\schema\`

## Directory Access Commands
```bash
# Navigate to target directory
cd {generic_path}
# Show directory structure
ls 
```

### File Operations
- Get the content of `BACGenericDeleteRecordObjInfos.xsd` in the `generic_path` directory
- Understand the structure and schema definitions in the file
- Make necessary modifications as per the requirements provided by the user
- Save the changes back to the same file


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

**OUTPUT LOCATION**:
- The generated `BatchPreviewDelegate` (if created) should be saved to the delegate output folder noted in `preview.md` (default: `.github/generated_delegates/`) or to `{preview}` if configured that way.

**VALIDATION**: Confirm `preview.md` exists and contains the sections above

### STEP 12: Delta Controller

## Directory Configuration
- `ba_path` = `\\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\com\ptc\windchill\bac\client\controllers\`

## Directory Access Commands
```bash
# Navigate to target directory
cd {ba_path}
# Show directory structure
ls -la
```
## DeltaController Addition Steps
- Ask User for Object Name to add DeltaController
- After getting Object Name from user, perform following steps
- Object_name = User Provided Object Name
- navigate to directory:
```bash
find . -name "*DeltaController*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```
- understand existing DeltaController patterns
- In method `categoryFromType(Class<?> clazz)`, add following code snippet:
```java
 if (Template.class.isAssignableFrom(clazz)) {
            return CollectionCategory.[TEMPLATE];
        }
```
- Add DeltaController for the provided Object Name
- add this object as a new constant in the DeltaController enum or class

**VALIDATION**:
- Confirm the DeltaController file is created/updated in the controllers directory
- Verify Java syntax for the modified file (or request build logs if compilation is required)
- If additional inputs are required from `deltacontroller.md`, prompt the user and stop until clarified

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
  - The required environment specifier for this build is `wnc_env urel_140`.
  - Run it inside the `WindchillVM` WSL distribution (non-interactive example):

```
wsl -d WindchillVM -- wnc_env urel_140
```

  - Or open an interactive session and run it there:

```
wsl -d WindchillVM
wnc_env urel_140
```

2. **Build BAC/src with Ant**:
  - Run the Ant build inside the `WindchillVM` WSL distro. Non-interactive one-liner:

```
wsl -d WindchillVM -- bash -lc "cd /opt/wnc/wcmod/modules/BAC/src && ant clean  clobber all"
```

  - Or interactively:

```
wsl -d WindchillVM
cd /opt/wnc/wcmod/modules/BAC/src
ant clean
ant clobber
ant all
exit
```

3. **Validation**:
  - Verify the Ant build completed without errors by checking the terminal output for BUILD SUCCESS messages.
  - If there are compilation errors, capture the first error block and report it; do not proceed further until resolved.

4. **Next steps**:
  - If you want, I can run these commands in a PowerShell terminal here (requires permission to execute terminal commands). Alternatively, you can copy the commands above and run them locally.
