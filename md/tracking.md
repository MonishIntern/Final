# DeleteTracking Delegate Creation Guide

### Overview
This guide provides comprehensive instructions for creating BAC delete tracking delegate classes that extend from BACDefaultGenericDeleteTrackingDelegate in the Windchill BAC (Business Administration Console) module.

### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing delete tracking delegate patterns and implementations**
- **ANALYZE delete tracking delegate structure and methodology**
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

### Directory Configuration
- `object_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/delegates/`
- `tracking_delegate_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/wt/[object_package]/bac/`
- `object. json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {object_path}

# Show directory structure
ls -la

# Find delete tracking delegate files specifically
find .  -name "*DeleteTracking*.java" -type f

# Show file count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr
```

### Delete Tracking Delegate File Discovery and Analysis Process
```bash
# Read Delete Tracking Delegate Java files
find . -name "*DeleteTracking*. java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**:  List all delete tracking delegate files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**:  Read that file completely and provide detailed analysis
4. **Fourth**:  Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which delete tracking delegate should be created
6. **Sixth**:  Identify base delegate class methods that need to be implemented
7. **Finally**: Generate a new delete tracking delegate class following identified patterns

### Object Dependencies Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available attributes of that object from `object.json`
3. **Third**: Ask user to select which attributes to include in the tracking delegate

### Delete Tracking Delegate Class Generation Steps
1. **First**: Create a new Java class file named `BAC[ObjectName]DeleteTrackingDelegate. java`
2. **Second**: Extend from `BACDefaultGenericDeleteTrackingDelegate`
3. **Third**: Implement core methods:  `filterDeletedObjs()`, `setAttributes()`, `getCollectionCategory()`
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Create object-specific JAXB classes for attribute storage
6. **Sixth**:  Create filtering logic for object selection
7. **Seventh**:  **Generate minimal business logic - focus on structure and method signatures**
8. **Finally**: Save the generated file in `output_folder`

### Delete Tracking Delegate Guidelines (Based on BACDocTemplateDeleteTrackingDelegate Pattern)

#### Class Structure
- **Package**: `[object_package]. bac`
- **Extends**: `BACDefaultGenericDeleteTrackingDelegate`
- **Logger**: Optional - not used in the example pattern

#### Core Methods to Implement

1. **filterDeletedObjs(WTCollection objsToDelete)**: Filter objects for tracking
   - Add `@Override` annotation
   - Create WTHashSet for filtered objects
   - Iterate through objects using persistableCollection()
   - Apply object-specific filtering logic
   - Return filtered collection

2. **setAttributes(BACGenericDeleteRecord deleteRecord, Persistable objBeingDel)**: Set tracking attributes
   - Add `@Override` and `protected` modifiers
   - Cast Persistable to specific object type
   - Set standard attributes directly on deleteRecord
   - Create object-specific JAXB info objects
   - Set object-specific attributes in JAXB objects
   - Create BACGenericDeleteRecordObjInfos and set it on deleteRecord
   - Handle WTPropertyVetoException with try-catch

3. **getCollectionCategory()**: Return collection category
   - Add `@Override` and `protected` modifiers
   - Return appropriate CollectionCategory enum value

#### Code Patterns to Follow

**filterDeletedObjs Pattern:**
```java
@Override
protected WTCollection filterDeletedObjs(WTCollection objsToDelete) {
    WTSet [objectName]TemplatesToDel = new WTHashSet(1);
    for ([ObjectType] obj : (Collection<[ObjectType]>) objsToDelete.persistableCollection()) {
        // TODO: Add object-specific filtering logic
        // Example: if (obj.isTemplated() && ! WorkInProgressHelper.isWorkingCopy(obj)) {
        //     [objectName]TemplatesToDel.add(obj);
        // }
    }
    return [objectName]TemplatesToDel;
}
```

**setAttributes Pattern:**
```java
@Override
protected void setAttributes(BACGenericDeleteRecord deleteRecord, Persistable objBeingDel) throws WTException {
    [ObjectType] templateObj = ([ObjectType]) objBeingDel;
    try {
        // Set standard attributes
        deleteRecord.setName(templateObj.getName());
        
        // Create object-specific info block
        {
            [ObjectName]ObjInfos objInfos = new [ObjectName]ObjInfos();
            objInfos.setName(templateObj.getName());
            // TODO: Set additional object-specific attributes

            BACGenericDeleteRecordObjInfos objInfosContainer = new BACGenericDeleteRecordObjInfos();
            objInfosContainer.set[ObjectName]ObjInfos(objInfos);
            deleteRecord.setObjInfosObject(objInfosContainer);
        }
    } catch (WTPropertyVetoException exc) {
        throw new WTException(exc);
    }
}
```

**getCollectionCategory Pattern:**
```java
@Override
protected CollectionCategory getCollectionCategory() {
    return CollectionCategory.[OBJECT_NAME];
}
```

#### Object Filtering Patterns

Common filtering logic patterns: 
- **Template Objects**: `obj.isTemplated()`
- **Non-Working Copies**: `!WorkInProgressHelper.isWorkingCopy(obj)`
- **Latest Iterations**: `obj.isLatestIteration()`
- **Specific States**: `obj.getState().equals(targetState)`
- **Container-based**: `obj.getContainer().equals(targetContainer)`

#### Attribute Setting Patterns

**Standard Attributes (directly on deleteRecord):**
```java
deleteRecord.setName(templateObj.getName());
deleteRecord.setContainerPath(IxbHndHelper.getPathOfContainer(templateObj.getContainerReference()));
```

**Object-Specific Attributes (through JAXB objects):**
```java
[ObjectName]ObjInfos objInfos = new [ObjectName]ObjInfos();
objInfos.setVersionName(VersionControlHelper.getIterationDisplayIdentifier(templateObj)
        .getLocalizedMessage(SessionHelper.getLocale()));
objInfos.setStateName(templateObj.getState().getDisplay());
objInfos.setTypeName(templateObj.getType().getDisplay());
```

#### JAXB Object Creation Pattern

1. **Create Object-Specific Info**:  `[ObjectName]ObjInfos objInfos = new [ObjectName]ObjInfos();`
2. **Set Attributes**: Use setter methods for each attribute
3. **Create Container**:  `BACGenericDeleteRecordObjInfos objInfosContainer = new BACGenericDeleteRecordObjInfos();`
4. **Set Container**: `objInfosContainer.set[ObjectName]ObjInfos(objInfos);`
5. **Set on Record**: `deleteRecord.setObjInfosObject(objInfosContainer);`

#### Helper Classes Reference

Common helper classes used in delete tracking delegates: 
- `IxbHndHelper` - For container path extraction
- `VersionControlHelper` - For version-related attributes
- `SessionHelper` - For locale information
- `WorkInProgressHelper` - For work-in-progress checks
- `StateHelper` - For state information

#### Collection Iteration Pattern

Use this pattern for safe collection iteration:
```java
for ([ObjectType] obj : (Collection<[ObjectType]>) objsToDelete.persistableCollection()) {
    // Process each object
}
```

#### Critical Rules

1. **DO NOT implement interface** - Always extend `BACDefaultGenericDeleteTrackingDelegate`
2. **Use WTHashSet for collections** - Initialize with appropriate capacity
3. **Cast collections properly** - Use (Collection<ObjectType>) pattern
4. **Handle WTPropertyVetoException** - Wrap in WTException
5. **Create JAXB objects in block scope** - Use {} to scope JAXB object creation
6. **Use helper classes** - For attribute extraction and validation
7. **Add @Override annotations** - For all overridden methods
8. **Use protected modifier** - For setAttributes and getCollectionCategory methods

- DO NOT add any more method than specified above
- If there is any method that is not specified above, add it as a comment with TODO for business logic
- Do not implement any business logic that is not specified above
- Do not read any other file after user provide a specific file name to read
- Do not create any super class method if it is not specified above
- Do not create any additional helper methods unless specified above

#### Exception Handling

- **WTPropertyVetoException**: Catch and wrap in WTException in setAttributes method
- **WTException**:  Declare throws WTException in setAttributes method
- **Other Exceptions**: Let propagate or handle as appropriate

#### Dependencies and Imports

```java
import java.util.Collection;
import com.ptc.windchill. bac.BACGenericDeleteRecord;
import com. ptc.windchill.bac.CollectionCategory;
import com.ptc.windchill.bac.delegates.BACDefaultGenericDeleteTrackingDelegate;
import com. ptc.windchill.bac.delete.jaxb.BACGenericDeleteRecordObjInfos;
import com.ptc. windchill.bac.delete.jaxb.[ObjectName]ObjInfos;
import wt.fc. Persistable;
import wt. fc.collections.WTCollection;
import wt.fc. collections.WTHashSet;
import wt.fc.collections.WTSet;
import wt. ixb.publicforhandlers.IxbHndHelper;
import wt.session.SessionHelper;
import wt.util.WTException;
import wt.util. WTPropertyVetoException;
import wt. vc.VersionControlHelper;
import wt.vc.wip.WorkInProgressHelper;
```

### Import Guidelines
- Include Collection for iteration patterns
- Include specific JAXB classes for object info storage
- Include helper classes for attribute extraction
- Include exception classes for proper error handling
- Do not include logging imports (not used in pattern)
- Ensure no unused imports are present

### JAXB Object Naming Convention

JAXB object classes follow this naming pattern:
- `[ObjectName]ObjInfos` - For storing object-specific attributes
- Example: `DocTemplateObjInfos`, `PartTemplateObjInfos`, `CustomObjectObjInfos`

The corresponding methods on BACGenericDeleteRecordObjInfos: 
- `set[ObjectName]ObjInfos()` - To set the object info
- Example: `setDocTemplateObjInfos()`, `setPartTemplateObjInfos()`

### Filtering Logic Guidelines

1. **Object Type Validation**: Check if object is of expected type
2. **Business Logic Filters**: Apply domain-specific filtering (templated, states, etc.)
3. **Work-in-Progress Checks**:  Exclude working copies if appropriate
4. **Iteration Checks**: Consider latest iteration requirements
5. **Container Validation**:  Validate container context if needed

### Attribute Setting Guidelines

1. **Standard Attributes First**: Set name, container path on deleteRecord directly
2. **Object-Specific Attributes**: Use JAXB objects for complex attributes
3. **Version Information**: Use VersionControlHelper for version attributes
4. **Localization**: Use SessionHelper. getLocale() for localized values
5. **Error Handling**: Wrap attribute setting in try-catch for WTPropertyVetoException

### Business Logic Guidelines
- **Minimal implementation**: Focus on structure and filtering patterns
- **Use TODO comments** for complex filtering logic
- **Ask user for filtering criteria** before generating filter logic
- **Keep filtering generic** for easy extension
- **Follow existing patterns** from analyzed delete tracking delegates
- **Use helper classes** for complex attribute extraction

### Method Signature Guidelines
- `filterDeletedObjs`: `protected WTCollection filterDeletedObjs(WTCollection objsToDelete)`
- `setAttributes`: `protected void setAttributes(BACGenericDeleteRecord deleteRecord, Persistable objBeingDel) throws WTException`
- `getCollectionCategory`: `protected CollectionCategory getCollectionCategory()`
- All methods should have `@Override` annotation

### Validation Checklist
Before finalizing the generated delete tracking delegate:
- [ ] Extends BACDefaultGenericDeleteTrackingDelegate (not implements interface)
- [ ] Contains proper package declaration for object package
- [ ] Includes all necessary imports for JAXB and helper classes
- [ ] Implements filterDeletedObjs with @Override annotation
- [ ] Uses WTHashSet for filtered collection
- [ ] Implements setAttributes with @Override and protected modifiers
- [ ] Creates appropriate JAXB objects for attribute storage
- [ ] Uses try-catch for WTPropertyVetoException
- [ ] Implements getCollectionCategory with correct CollectionCategory
- [ ] Uses helper classes for attribute extraction
- [ ] Handles collection iteration safely with Collection casting
- [ ] No unused imports or unnecessary code
- [ ] TODO comments mark uncertain business logic