# DeleteRecordAttributes Creation Guide

### Overview
This guide provides comprehensive instructions for creating BAC delete record attributes classes that extend from BACDeleteRecordAttributes in the Windchill BAC (Business Administration Console) module.


## Save as
- BAC[ObjectName]DeleteRecordAttributes.java in output_folder


### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing delete record attributes patterns and implementations**
- **ANALYZE delete record attributes structure and methodology**
- **GENERATE similar delete record attributes for user-specified object**
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
- **Collection Category**: Use appropriate enum from `CollectionCategory` which is uppercase of object name

### Directory Configuration
- `object_path` = `//wsl. localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/delegates/`
- `delete_record_attr_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/wt/[object_package]/bac/`
- `object. json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {object_path}

# Show directory structure
ls -la

# Find delete record attributes files specifically
find . -name "*DeleteRecordAttributes*. java" -type f

# Show file count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr
```

### Delete Record Attributes File Discovery and Analysis Process
```bash
# Read Delete Record Attributes Java files
find . -name "*DeleteRecordAttributes*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**:  List all delete record attributes files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**:  Read that file completely and provide detailed analysis
4. **Fourth**:  Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which delete record attributes should be created
6. **Sixth**:  Identify required identity attributes and value extraction patterns
7. **Finally**: Generate a new delete record attributes class following identified patterns

### Object Attributes Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available attributes of that object from `object.json`
3. **Third**: Ask user to select which attributes to include as identity attributes
4. **Fourth**: Ask user about the value extraction pattern for each selected attribute

### Delete Record Attributes Class Generation Steps
1. **First**: Create a new Java class file named `BAC[ObjectName]DeleteRecordAttributes.java`
2. **Second**: Determine required identity attributes based on corresponding delete record class
3. **Third**: Implement core methods:  constructor, `getIdentityAttributesWithValues()`
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Add static field declarations for custom attributes
6. **Sixth**:  Create attribute value extraction logic
7. **Seventh**: **Generate minimal business logic - focus on structure and method signatures**
8. **Finally**: Save the generated file in `output_folder`

### Delete Record Attributes Guidelines (Based on BACDocTemplateDeleteRecordAttributes Pattern)

#### Class Structure
- **Package**: `wt.[object_package]. bac`
- **Extends**: `BACDeleteRecordAttributes` (not implements interface)
- **Static Fields**: Declare constants for custom attribute names
- **Logger**: Optional - not used in the example pattern
- **Collection Category**: Use appropriate enum from `CollectionCategory` which is uppercase of object name

#### Static Field Declarations
Declare static final fields for attribute names:
```java
private final static String ATTRIBUTE_NAME = SearchableByInterface.ATTRIBUTE_NAME;
```

Common patterns:
- `private final static String VERSION_NAME = SearchableByVersion. VERSION_NAME;`
- `private final static String STATE_NAME = SearchableByState.STATE_NAME;`
- `private final static String TYPE_NAME = SearchableByType. TYPE_NAME;`

#### Core Methods to Implement

1. **Constructor**:  Initialize identity attributes
   - Create new `HashSet<String>` for identity attributes
   - Add all identity attribute names to the set
   - Use inherited constants like `NAME`, `CONTAINER_PATH` from base class
   - Use custom static fields for additional attributes

2. **getIdentityAttributesWithValues(BACGenericDeleteRecord delRec)**: Extract attribute values
   - Must be `protected` method with `@Override` annotation
   - Create new `LinkedHashMap<String, String>` for identity map
   - Extract values from `delRec` using appropriate getter methods
   - Return the populated identity map

#### Code Patterns to Follow

**Constructor Pattern:**
```java
public BAC[ObjectName]DeleteRecordAttributes() {
    // Ref Identity of BAC[ObjectName]DeleteRecord
    Set<String> identityAttributes = new HashSet<>();
    identityAttributes.add(NAME);
    identityAttributes.add(CONTAINER_PATH);
    identityAttributes.add(VERSION_NAME);
    // TODO: Add other identity attributes based on user selection
}
```

**getIdentityAttributesWithValues Pattern:**
```java
@Override
protected LinkedHashMap<String, String> getIdentityAttributesWithValues(BACGenericDeleteRecord delRec)
        throws WTException {
    LinkedHashMap<String, String> identityMap = new LinkedHashMap<>();
    identityMap.put(NAME, delRec. getName());
    // TODO: Add other attribute value extractions based on user selection
    return identityMap;
}
```

#### Attribute Value Extraction Patterns

**Standard Attributes (from base class):**
- `delRec.getName()` - For NAME attribute


#### Identity Attributes Mapping
Map identity attributes to their corresponding searchable interfaces:
- `NAME` - Available from base class (SearchableByName)
- `CONTAINER_PATH` - Available from base class (SearchableByContainer)
- `VERSION_NAME` - From SearchableByVersion interface
- `STATE_NAME` - From SearchableByState interface
- `TYPE_NAME` - From SearchableByType interface

#### Base Class Constants
Available constants from `BACDeleteRecordAttributes` base class:
- `NAME` - Object name attribute
- `CONTAINER_PATH` - Container path attribute

These can be used directly without importing or declaring static fields.

#### Critical Rules

1. **DO NOT implement interface** - Always extend `BACDeleteRecordAttributes`
2. **Use HashSet in constructor** - For identity attributes initialization
3. **Use LinkedHashMap for return value** - Maintains insertion order
4. **Method must be protected** - Not public
5. **Add @Override annotation** - For getIdentityAttributesWithValues method
6. **Use static final fields** - For custom attribute name constants
7. **Follow ObjInfosObject pattern** - For object-specific attribute extraction
8. **Handle WTException** - Declare throws WTException in method signature

- DO NOT add any more method than specified above
- If there is any method that is not specified above, add it as a comment with TODO for business logic
- Do not implement any business logic that is not specified above
- Do not read any other file after user provide a specific file name to read 
- Do not create any super class method if it is not specified above
- Do not create any additional helper methods unless specified above

#### Exception Handling
- Declare `throws WTException` in getIdentityAttributesWithValues method signature
- No explicit try-catch needed in the example pattern
- Let exceptions propagate to caller

#### Dependencies and Imports
```java
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Set;
import com.ptc.windchill. bac.BACDeleteRecordAttributes;
import com.ptc.windchill.bac. BACGenericDeleteRecord;
import com.ptc.windchill.bac.search.SearchableByVersion;
import com.ptc.windchill. bac.search.SearchableByState;
import com.ptc.windchill. bac.search.SearchableByType;
import wt.util.WTException;
```

### Import Guidelines
- Include java.util imports for HashSet and LinkedHashMap
- Include specific searchable interface imports for custom attributes
- Include BACDeleteRecordAttributes and BACGenericDeleteRecord
- Include WTException for exception handling
- Do not include logging imports (not used in pattern)
- Ensure no unused imports are present

### Object-Specific Value Extraction Guide

The pattern for extracting object-specific attribute values follows this structure: 
```java
delRec.getObjInfosObject().get[ObjectName]ObjInfos().[getAttributeMethod]()
```

Examples:
- Document Template:  `delRec.getObjInfosObject().getDocTemplateObjInfos().getVersionName()`
- Part Template: `delRec.getObjInfosObject().getPartTemplateObjInfos().getVersionName()`
- Custom Object: `delRec.getObjInfosObject().get[CustomObject]ObjInfos().getVersionName()`

### Constructor Implementation Guide

1. **Create HashSet**:  Initialize with appropriate capacity
2. **Add Base Attributes**: Use inherited constants (NAME, CONTAINER_PATH)
3. **Add Custom Attributes**: Use declared static fields
4. **Order Matters**: Add attributes in logical order (name, container, version, state, type)

Example order:
```java
identityAttributes.add(NAME);                // Always first
```

### Value Extraction Implementation Guide

1. **Create LinkedHashMap**:  Maintains insertion order for consistent output
2. **Extract Standard Values**: Use direct getter methods from delRec
3. **Extract Object-Specific Values**: Use ObjInfosObject pattern
4. **Match Constructor Order**: Put values in same order as constructor adds attributes
5. **Handle Null Values**:  Consider null checks if attributes might be null

### Business Logic Guidelines
- **Minimal implementation**: Focus on structure and attribute mapping
- **Use TODO comments** for complex value extraction logic
- **Ask user for attribute selection** before generating extraction code
- **Keep attributes mapping generic** for easy extension
- **Follow existing patterns** from analyzed delete record attributes files
- **Use consistent naming conventions** for static fields

### Static Field Naming Guidelines
- Use `UPPER_CASE_WITH_UNDERSCORES` for static final fields
- Match the constant name from corresponding searchable interface
- Example: `SearchableByVersion.VERSION_NAME` becomes `VERSION_NAME`
- Declare as `private final static String` for consistency

### Method Signature Guidelines
- Constructor: `public BAC[ObjectName]DeleteRecordAttributes()`
- Attribute method: `protected LinkedHashMap<String, String> getIdentityAttributesWithValues(BACGenericDeleteRecord delRec) throws WTException`
- Use exact parameter and return types as shown
- Include @Override annotation for overridden method

### Validation Checklist
Before finalizing the generated delete record attributes:  
- [ ] Extends BACDeleteRecordAttributes (not implements interface)
- [ ] Contains proper package declaration for object package
- [ ] Includes all necessary imports for selected attributes
- [ ] Declares static final fields for custom attributes
- [ ] Implements constructor with HashSet initialization
- [ ] Adds all identity attributes to HashSet in constructor
- [ ] Implements getIdentityAttributesWithValues with @Override
- [ ] Uses LinkedHashMap for return value
- [ ] Extracts values using appropriate patterns (direct or ObjInfosObject)
- [ ] Maintains consistent attribute order in constructor and method
- [ ] Declares throws WTException in method signature
- [ ] No unused imports or unnecessary code
- [ ] TODO comments mark uncertain attribute extractions
