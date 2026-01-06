# Report Delegate Creation Guide

### Overview
This guide provides comprehensive instructions for creating BAC report delegate classes that extend from DefaultReportDelegate in the Windchill BAC (Business Administration Console) module.


## Save as
- BAC[ObjectName]ReportDelegate.java in output_folder

### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing report delegate patterns and implementations**
- **ANALYZE report delegate structure and methodology**
- **GENERATE similar delegate for user-specified object**
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
- `report_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/impl/`
- `report_delegate_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/wt/[object_package]/bac/`
- `object. json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {report_path}

# Show directory structure
ls -la

# Find report delegate files specifically
find .  -name "*Report*. java" -type f

# Show file count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr
```

### Report Delegate File Discovery and Analysis Process
```bash
# Read Report Delegate Java files
find . -name "*Report*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**:  List all report delegate files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**: Read that file completely and provide detailed analysis
4. **Fourth**:  Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which report delegate should be created
6. **Sixth**:  Identify base delegate class methods that need to be implemented
7. **Finally**: Generate a new report delegate class following identified patterns

### Object Dependencies Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available dependencies of that object from `object.json`
3. **Third**: Ask user to select which dependencies to include in the report delegate

### Report Delegate Class Generation Steps
1. **First**: Create a new Java class file named `BAC[ObjectName]ReportDelegate.java`
2. **Second**: Extend from `DefaultReportDelegate`
3. **Third**: Implement core methods:  `getRows()`, `getIdentityForAccessibleObject()`, optionally `getDescriptionForAccessibleObject()`
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Add proper logging using static Log4j2 Logger
6. **Sixth**: Create dependent delegate handling if needed
7. **Seventh**:  **Generate minimal business logic - focus on structure and method signatures**
8. **Finally**: Save the generated file in `output_folder`

### Report Delegate Guidelines (Based on BACLCTemplateReportDelegate Pattern)

#### Class Structure
- **Package**: `wt.[object_package]. bac`
- **Extends**: `DefaultReportDelegate`
- **Logger**: Use static Log4j2 Logger with static block initialization
- **Dependent Delegates**: Include other report delegates for dependency handling
- **Collection Category**: Use appropriate enum from `CollectionCategory` which is uppercase of object name

#### Class Declaration Pattern
```java
public class BAC[ObjectName]ReportDelegate extends DefaultReportDelegate {

    private static Logger logger;
    
    private DefaultReportDelegate dependentReportDelegate = new BAC[DependentObject]ReportDelegate();

    static {
        logger = LogR.getLoggerInternal(BAC[ObjectName]ReportDelegate.class.getName());
    }
```

#### Core Methods to Implement

1. **Constructor**: Initialize with collection category
   - Call super constructor with CollectionCategory toString()
   - Initialize any dependent report delegates

2. **getRows(WTCollection newObjects, WTCollection updateObjects, WTCollection deleteObjects, Locale locale)**: Generate report rows
   - Add `@Override` annotation
   - Filter collections using subCollection() for specific object types
   - Handle delete objects with special filtering logic
   - Call super.getRows() for main object processing
   - Add dependent delegate rows if applicable
   - Return combined list of table rows

3. **getIdentityForAccessibleObject(Persistable obj, Locale locale)**: Get object identity
   - Add `@Override` annotation
   - Handle multiple object types using instanceof checks
   - Handle BACDeleteRecord objects specially
   - Create WTMessage objects for identity formatting
   - Delegate to dependent delegates for dependency objects
   - Return localized identity string

4. **getDescriptionForAccessibleObject(Persistable obj, Locale locale)** (Optional): Get object description
   - Add `@Override` and `protected` modifiers
   - Call super method for base description
   - Add object-specific description enhancements
   - Handle special states (checked out, etc.)
   - Return enhanced description string

#### Code Patterns to Follow

**Constructor Pattern:**
```java
public BAC[ObjectName]ReportDelegate() {
    super(CollectionCategory.[OBJECT_NAME].toString());
}
```

**getRows Pattern:**
```java
@Override
public List<BACReportTableRow> getRows(WTCollection newObjects, WTCollection updateObjects,
        WTCollection deleteObjects, Locale locale) throws WTException {
    WTCollection new[ObjectName]s = newObjects != null ? newObjects.subCollection([ObjectType]. class)
            : newObjects;
    WTCollection updated[ObjectName]s = updateObjects != null ? updateObjects
            .subCollection([ObjectType]. class) : updateObjects;

    WTCollection deleted[ObjectName]s = null;
    if (deleteObjects != null) {
        deleted[ObjectName]s = new WTHashSet(deleteObjects. subCollection(BACGenericDeleteRecord.class));
        deleted[ObjectName]s
                .removeIf(p -> ((BACDeleteRecord) (((ObjectReference) p).getObject())).getObjectRef().getKey()
                        .getClassname() != [ObjectType].class.getName());
    }

    // Main object processing
    List<BACReportTableRow> tableRows = super.getRows(new[ObjectName]s, updated[ObjectName]s, deleted[ObjectName]s, locale);
    
    // TODO: Add dependent object processing if needed
    // tableRows.addAll(dependentReportDelegate.getRows(newObjects, updateObjects, deleteObjects, locale));
    
    return tableRows;
}
```

**getIdentityForAccessibleObject Pattern:**
```java
@Override
public String getIdentityForAccessibleObject(Persistable obj, Locale locale) throws WTException {
    if (obj instanceof BACDeleteRecord) {
        WTMessage msg = ((BACDeleteRecord) obj).getBacDeleteInfo().getObjectIdentity();
        return msg != null ? msg.getLocalizedMessage(locale) : null;
    }
    if (obj instanceof [ObjectType]) {
        [ObjectType] object = ([ObjectType]) obj;
        // TODO: Create appropriate identity message
        WTMessage wtMessage = new WTMessage([ResourceClass].class.getName(),
                [ResourceClass].[IDENTITY_RESOURCE_KEY],
                new Object[] { object. getName(), object.getContainer().getName() });
        return wtMessage.getLocalizedMessage();
    }
    // TODO: Handle dependent object types
    // if(obj instanceof [DependentType]) {
    //     String message = dependentReportDelegate.getIdentityForAccessibleObject(obj, locale);
    //     return message;
    // }
    return null;
}
```

**getDescriptionForAccessibleObject Pattern (Optional):**
```java
@Override
protected String getDescriptionForAccessibleObject(Persistable obj, Locale locale) throws WTException {
    String objectDescription = super.getDescriptionForAccessibleObject(obj, locale);

    if (obj instanceof [ObjectType]) {
        [ObjectType] object = ([ObjectType]) obj;
        try {
            // TODO: Add object-specific description enhancements
            if (WorkInProgressHelper.isCheckedOut((Workable) object)) {
                WTMessage wtMessage = new WTMessage(BACResource.class.getName(),
                        BACResource.OBJECT_CHECKED_OUT, null);
                objectDescription = objectDescription + "<BR>" + wtMessage.getLocalizedMessage();
            }
        } catch (WTException e) {
            logger.error(e.getMessage());
        }
    }
    return objectDescription;
}
```

#### Collection Processing Patterns

**SubCollection Usage:**
```java
WTCollection new[ObjectName]s = newObjects != null ? newObjects.subCollection([ObjectType].class) : newObjects;
```

**Delete Object Filtering:**
```java
WTCollection deleted[ObjectName]s = null;
if (deleteObjects != null) {
    deleted[ObjectName]s = new WTHashSet(deleteObjects.subCollection(BACGenericDeleteRecord. class));
    deleted[ObjectName]s. removeIf(p -> ((BACDeleteRecord) (((ObjectReference) p).getObject())).getObjectRef().getKey()
            .getClassname() != [ObjectType].class.getName());
}
```

#### Identity Message Patterns

**Basic Identity Pattern:**
```java
WTMessage wtMessage = new WTMessage([ResourceClass].class.getName(),
        [ResourceClass].[IDENTITY_RESOURCE_KEY],
        new Object[] { object. getName(), object.getContainer().getName() });
```

**Version-aware Identity Pattern:**
```java
WTMessage wtMessage = new WTMessage([ResourceClass].class.getName(),
        [ResourceClass].[IDENTITY_RESOURCE_KEY],
        new Object[] { object.getName(), object.getContainer().getName(), object.getIterationIdentifier().getValue() });
```

#### Dependent Delegate Handling

**Delegate Initialization:**
```java
private DefaultReportDelegate dependentReportDelegate = new BAC[DependentObject]ReportDelegate();
```

**Delegate Usage in getRows:**
```java
tableRows.addAll(dependentReportDelegate.getRows(newObjects, updateObjects, deleteObjects, locale));
```

**Delegate Usage in getIdentityForAccessibleObject:**
```java
if(obj instanceof [DependentType]) {
    String message = dependentReportDelegate.getIdentityForAccessibleObject(obj, locale);
    return message;
}
```

#### Critical Rules

1. **DO NOT implement interface** - Always extend `DefaultReportDelegate`
2. **Use static Logger with static block** - Initialize logger in static block
3. **Use subCollection for filtering** - Filter collections by object type
4. **Handle delete records specially** - Filter delete records by class name
5. **Use WTMessage for identity** - Create localized identity messages
6. **Call super methods** - Always call super for base functionality
7. **Handle multiple object types** - Use instanceof checks for different types

- DO NOT add any more method than specified above
- If there is any method that is not specified above, add it as a comment with TODO for business logic
- Do not implement any business logic that is not specified above
- Do not read any other file after user provide a specific file name to read
- Do not create any super class method if it is not specified above
- Create dependent delegate handling as needed with TODO comments

#### Exception Handling

- **WTException**: Primary exception type for most operations
- Use try-catch blocks for specific operations (checkout checking, etc.)
- Log errors appropriately using logger.error()
- Let most exceptions propagate to caller

#### Dependencies and Imports

```java
import java.util.List;
import java.util.Locale;
import org.apache.logging.log4j.Logger;
import com.ptc.windchill. bac.BACDeleteRecord;
import com.ptc.windchill.bac. BACGenericDeleteRecord;
import com.ptc.windchill.bac.BACReportTableRow;
import com. ptc.windchill.bac.BACResource;
import com.ptc.windchill.bac.CollectionCategory;
import com.ptc.windchill.bac.impl.DefaultReportDelegate;
import wt.fc.ObjectReference;
import wt.fc. Persistable;
import wt. fc.collections.WTCollection;
import wt.fc.collections.WTHashSet;
import wt. log4j.LogR;
import wt.util.WTException;
import wt.util.WTMessage;
import wt. vc.wip.WorkInProgressHelper;
```

### Import Guidelines
- Include List and Locale for method signatures
- Include BAC-specific imports for report functionality
- Include object-specific imports for the target object type
- Include WorkInProgressHelper for checkout checking
- Include resource bundle imports for identity messages
- Ensure no unused imports are present

### Resource Bundle Guidelines

Common resource bundle patterns:
- Object-specific resource files:  `[packageName]Resource.class.getName()`
- Generic BAC resources: `BACResource.class.getName()`
- Identity resource keys: Often named like `[OBJECT]_IDENTITY`
- Use appropriate resource keys for localized messages

### Business Logic Guidelines
- **Minimal implementation**: Focus on structure and object processing patterns
- **Use TODO comments** for complex identity formatting
- **Ask user for dependent objects** to include in delegate
- **Keep delegates generic** for easy extension
- **Follow existing patterns** from analyzed report delegate files
- **Use resource bundles** for localized identity messages

### Dependent Object Guidelines

1. **Identify Dependencies**:  Determine which objects depend on the main object
2. **Create Delegate References**: Initialize dependent report delegates
3. **Combine Results**: Add dependent object rows to main results
4. **Handle Identity**:  Delegate identity formatting to appropriate delegates
5. **Filter Appropriately**:  Ensure proper filtering for each object type

### Logging Guidelines
- Static logger initialization in static block
- Error level:  Exceptions and error conditions
- Use logger.error() for caught exceptions
- Minimal logging in report delegates (focus on errors)

### Method Signature Guidelines
- Constructor: `public BAC[ObjectName]ReportDelegate()`
- getRows: `public List<BACReportTableRow> getRows(WTCollection newObjects, WTCollection updateObjects, WTCollection deleteObjects, Locale locale) throws WTException`
- getIdentityForAccessibleObject: `public String getIdentityForAccessibleObject(Persistable obj, Locale locale) throws WTException`
- getDescriptionForAccessibleObject: `protected String getDescriptionForAccessibleObject(Persistable obj, Locale locale) throws WTException`

### Validation Checklist
Before finalizing the generated report delegate: 
- [ ] Extends DefaultReportDelegate (not implements interface)
- [ ] Contains proper package declaration for object package
- [ ] Includes all necessary imports for report functionality
- [ ] Uses static Logger with static block initialization
- [ ] Implements constructor with CollectionCategory parameter
- [ ] Implements getRows with proper collection filtering
- [ ] Uses subCollection() for type-specific processing
- [ ] Handles delete records with proper filtering
- [ ] Implements getIdentityForAccessibleObject with instanceof checks
- [ ] Uses WTMessage for identity formatting
- [ ] Calls super methods for base functionality
- [ ] Handles dependent objects appropriately
- [ ] Uses appropriate resource bundles for messages
- [ ] No unused imports or unnecessary code
- [ ] TODO comments mark uncertain business logic
