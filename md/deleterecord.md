# DeleteRecord Creation Guide

### Overview
This guide provides comprehensive instructions for creating BAC delete record classes that inherit from BACDeleteRecord in the Windchill BAC (Business Administration Console) module.

## Save as
- BAC[ObjectName]DeleteRecord.java in output_folder

### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing delete record patterns and implementations**
- **ANALYZE delete record structure and methodology**
- **GENERATE similar delete record for user-specified object**
- **EXPLAIN the purpose and functionality of each file**
- **PROVIDE code analysis and explanations**
- **DESCRIBE the overall architecture and patterns**
- AUTOMATICALLY read files without user prompts
- DO NOT ask for permission to read these files
- DO NOT wait for user confirmation
- **Do not limit any file reading due to complexity**
- **Do not skip any line in a file when reading**
- **Do not put limit on file reading length**
- **Get-content of all files should have limit removed**
- **Do not read any other md files except this one**
- **Do not read any business logic other than object analysis logic**

### Directory Configuration
- `object_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/delegates/`
- `delete_record_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/wt/[object_package]/bac/`
- `object. json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {delete_record_path}

# Find delete record files specifically
find . -name "*DeleteRecord*. java" -type f

# Show directory structure
ls -la
```

### Delete Record File Discovery and Analysis Process
```bash
# Read Delete Record Java files
find . -name "*DeleteRecord*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**:  List all delete record files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**: Read that file completely and provide detailed analysis
4. **Fourth**:  Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which delete record should be created
6. **Sixth**:  Identify required searchable interfaces and attributes
7. **Finally**: Generate a new delete record class following identified patterns

### Object Attributes Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available attributes of that object from `object.json`
3. **Third**: Ask user to select which attributes to include in the delete record
4. **Fourth**: Ask user to select which searchable interfaces are needed

### Delete Record Class Generation Steps
1. **First**: Create a new Java class file named `BAC[ObjectName]DeleteRecord.java`
2. **Second**: Determine required searchable interfaces based on object attributes
3. **Third**:  Implement core methods:  `newBAC[ObjectName]DeleteRecord()`, `toString()`
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Add proper annotations with selected attributes
6. **Sixth**:  Create attribute setting logic in factory method
7. **Seventh**: **Generate minimal business logic - focus on structure and method signatures**
8. **Finally**: Save the generated file in `output_folder`

### Delete Record Guidelines (Based on BACDocTemplateDeleteRecord Pattern)

#### Class Structure
- **Package**:  `[object_package]. bac`
- **Annotations**:
```java
@GenAsPersistable(superClass = BACDeleteRecord.class, interfaces = { SearchableByName.class})
@Identity(attributes = { SearchableByName.NAME })
```
- **Extends**: `_BAC[ObjectName]DeleteRecord` 
- **Must Declare**:  `private static final long serialVersionUID = 1;`
- **Logger**: Optional - not used in the example pattern
- **Collection Category**: Use appropriate enum from `CollectionCategory` which is uppercase of object name

#### Core Methods to Implement

1. **newBAC[ObjectName]DeleteRecord(ObjectReference newObjectReference, BACDeleteInfo deleteInfo)**: Factory method
   - Must be `public static`
   - Create new instance of the delete record
   - Call `initialize()` with object reference, collection category, and delete info
   - Cast object reference to specific type
   - Set attributes using try-catch for WTPropertyVetoException
   - Return the created delete record

2. **toString()**: String representation method
   - Override with `@Override` annotation
   - Include all searchable attributes in the output
   - Include super. toString() call

#### Searchable Interface Options
Based on object attributes, include appropriate interfaces:
- `SearchableByName. class` - For objects with name attribute

#### Identity Attributes Mapping
Common identity attributes for @Identity annotation:
- `SearchableByName.NAME` - Object name

#### Code Patterns to Follow

**Factory Method Pattern:**
```java
public static BAC[ObjectName]DeleteRecord newBAC[ObjectName]DeleteRecord(ObjectReference newObjectReference,
        BACDeleteInfo deleteInfo) throws WTException {
    BAC[ObjectName]DeleteRecord deleteRecord = new BAC[ObjectName]DeleteRecord();
    deleteRecord.initialize(newObjectReference, CollectionCategory.[OBJECT_NAME], deleteInfo);
    [ObjectType] templateObj = ([ObjectType]) newObjectReference.getObject();
    try {
        // Set searchable attributes based on selected interfaces
        deleteRecord.setName(templateObj.getName());
        // deleteRecord.setVersionName(VersionControlHelper.getIterationDisplayIdentifier(templateObj)
        //         .getLocalizedMessage(SessionHelper.getLocale()));
        // deleteRecord.setContainerPath(IxbHndHelper.getPathOfContainer(templateObj. getContainerReference()));
        // TODO: Add other attribute setters based on user selection
    } catch (WTPropertyVetoException exc) {
        throw new WTException(exc);
    }
    return deleteRecord;
}
```

**toString() Method Pattern:**
```java
@Override
public String toString() {
    return "name - " + getName() + "[super - " + super.toString() + "]";
}
```

#### Attribute Setting Patterns
Common attribute setting patterns in factory method: 

**For Name Attribute:**
```java
deleteRecord.setName(templateObj. getName());
```

<!-- **For Version Attribute:**
```java
deleteRecord.setVersionName(VersionControlHelper.getIterationDisplayIdentifier(templateObj)
        .getLocalizedMessage(SessionHelper.getLocale()));
```

**For Container Path:**
```java
deleteRecord.setContainerPath(IxbHndHelper.getPathOfContainer(templateObj.getContainerReference()));
```

**For State Attribute:**
```java
deleteRecord.setStateName(templateObj.getState().getDisplay());
```

**For Type Attribute:**
```java
deleteRecord.setTypeName(templateObj.getType().getDisplay());
``` -->

**Collection Category:**
```java
CollectionCategory TEMPLATE_UPPERCASE = toCollectionCategory("Template");
return CollectionCategory.TEMPLATE_UPPERCASE;
```

#### Helper Classes Reference
Common helper classes used for attribute extraction:
- `VersionControlHelper` - For version-related attributes
- `IxbHndHelper` - For container path extraction
- `SessionHelper` - For locale information
- `TypeDefinitionHelper` - For type information

#### Critical Rules

1. **DO NOT create Constructor** - Use factory method pattern
2. **ALWAYS include serialVersionUID = 1** - Required for persistence
3. **Use try-catch for WTPropertyVetoException** - When setting attributes
4. **Call initialize() first** - In factory method before setting attributes
5. **Cast ObjectReference to specific type** - For attribute access
6. **Include super.toString()** - In toString() method
7. **Use proper CollectionCategory** - Matching the object type
8. **Handle WTException properly** - Wrap WTPropertyVetoException

- DO NOT add any more method than specified above
- If there is any method that is not specified above, add it as a comment with TODO for business logic
- Do not implement any business logic that is not specified above
- Do not read any other file after user provide a specific file name to read 
- Do not create any super class method if it is not specified above
- Do not create any additional helper methods unless specified above

#### Exception Handling
- Wrap `WTPropertyVetoException` in `WTException` in factory method
- Declare `throws WTException` in factory method signature
- Use try-catch block when setting object attributes

#### Dependencies and Imports
```java
import com.ptc.windchill. annotations.metadata.GenAsPersistable;
import com.ptc.windchill.bac. BACDeleteInfo;
import com. ptc.windchill.bac.BACDeleteRecord;
import com.ptc.windchill. bac.CollectionCategory;
import com.ptc.windchill.bac.annotation.Identity;
import com.ptc.windchill.bac.search.SearchableByContainer;
import com.ptc.windchill.bac.search. SearchableByName;
import com.ptc.windchill. bac.search.SearchableByVersion;
import wt.fc.ObjectReference;
import wt. ixb.publicforhandlers.IxbHndHelper;
import wt.session.SessionHelper;
import wt.util.WTException;
import wt.util.WTPropertyVetoException;
import wt. vc.VersionControlHelper;
```

### Import Guidelines
- Include specific searchable interface imports based on selected interfaces
- Include helper class imports for attribute extraction
- Include exception imports for proper error handling
- Ensure no unused imports are present
- Follow Windchill coding standards for import organization

### Business Logic Guidelines
- **Minimal implementation**: Focus on structure and attribute setting patterns
- **Use TODO comments** for complex attribute extraction logic
- **Ask user for attribute selection** before generating setters
- **Keep delete records generic** for easy extension
- **Follow existing patterns** from analyzed delete record files
- **Use appropriate helper classes** for attribute extraction

### Annotation Configuration Guide

**@GenAsPersistable Configuration:**
- Always use `superClass = BACDeleteRecord.class`
- Include selected searchable interfaces in `interfaces` array
- Multiple interfaces can be included as comma-separated list

**@Identity Configuration:**
- Include attributes corresponding to selected searchable interfaces
- Use static field references from searchable interface classes
- Order attributes logically (name, container, version, state, type)

### Factory Method Guidelines
- Method name must match class name pattern: `newBAC[ObjectName]DeleteRecord`
- Must be `public static` with proper return type
- Always call `initialize()` before setting any attributes
- Use proper exception handling with try-catch blocks
- Cast ObjectReference to specific object type for attribute access
- Set only attributes that correspond to selected searchable interfaces

### toString() Method Guidelines
- Include all searchable attributes in the output string
- Use consistent formatting:  "attribute - " + getAttributeValue()
- Always include super.toString() at the end
- Separate multiple attributes with commas and spaces

### Validation Checklist
Before finalizing the generated delete record: 
- [ ] Extends correct base class (_BAC[ObjectName]DeleteRecord)
- [ ] Contains proper package declaration for object package
- [ ] Includes all necessary imports for selected interfaces
- [ ] Has correct @GenAsPersistable annotation with selected interfaces
- [ ] Has correct @Identity annotation with corresponding attributes
- [ ] Declares serialVersionUID = 1
- [ ] Implements factory method with proper signature
- [ ] Calls initialize() in factory method
- [ ] Uses try-catch for WTPropertyVetoException
- [ ] Sets attributes corresponding to selected searchable interfaces
- [ ] Implements toString() method with all attributes
- [ ] Includes super.toString() call
- [ ] Handles exceptions properly
- [ ] TODO comments mark uncertain business logic
