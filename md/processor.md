# DeleteProcessor Creation Guide

### Overview
This guide provides comprehensive instructions for creating BAC delete processor classes that extend from BACDeleteProcessor in the Windchill BAC (Business Administration Console) module.


## Save as
- BAC[ObjectName]DeleteProcessor.java in output_folder

### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing delete processor patterns and implementations**
- **ANALYZE delete processor structure and methodology**
- **GENERATE similar processor for user-specified object**
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
- `object_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/delegates/`
- `processor_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/wt/[object_package]/bac/`
- `object.  json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {object_path}

# Show directory structure
ls -la

# Find delete processor files specifically
find .  -name "*DeleteProcessor*.  java" -type f

# Show file count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr
```

### Delete Processor File Discovery and Analysis Process
```bash
# Read Delete Processor Java files
find . -name "*DeleteProcessor*. java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**:  List all delete processor files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**:  Read that file completely and provide detailed analysis
4. **Fourth**:  Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**:  After reading all files, ask user for the Object for which delete processor should be created
6. **Sixth**:  Identify base delegate class methods that need to be implemented
7. **Finally**: Generate a new delete processor class following identified patterns

### Object Dependencies Extraction and Selection
1. **First**:  After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available attributes and dependencies of that object from `object.json`
3. **Third**: Ask user to select which attributes and conflict types to include

### Delete Processor Class Generation Steps
1. **First**: Create a new Java class file named `BAC[ObjectName]DeleteProcessor.java`
2. **Second**: Extend from `BACDeleteProcessor`
3. **Third**: Implement core methods and conflict handling logic
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Add proper logging using static Log4j2 Logger
6. **Sixth**:  Create private helper methods for conflict resolution
7. **Seventh**:  **Generate minimal business logic - focus on structure and method signatures**
8. **Finally**: Save the generated file in `output_folder`

### Delete Processor Guidelines (Based on BACDocTemplateDeleteProcessor Pattern)

#### Class Structure
- **Package**: `[object_package].bac`
- **Extends**: `BACDeleteProcessor`
- **Logger**: Use static Log4j2 Logger:  `LogR.getLoggerInternal(ClassName. class.getName())`
- **Private Fields**:
  - `Map<ObjectIdentifier, List<ConflictType>> oidToConflictMap` - Track conflicts by object ID
  - `Map<ConflictType, String> conflictTypeToMessage` - Track conflict messages
- **Collection Category**: Use appropriate enum from `CollectionCategory` which is uppercase of object name

#### Core Methods to Implement

1. **getConflictElements(FederationActionRequest request, List<Map<String, String>> objParamMap)**: Handle conflicts
   - Add `@Override` annotation
   - Call super method and add to result list
   - Clear conflict tracking maps
   - Find objects and check for conflicts
   - Create conflict elements with appropriate resolutions
   - Return complete conflict element list

2. **findByIdentityParams(List<Map<String, String>> objParamMapList)**: Find objects by identity
   - Add `@Override` and `protected` modifiers
   - Add debug logging for method entry
   - Create result map for found objects
   - Add TODO comment for actual implementation
   - Return result map

3. **getObjType()**: Return object type string
   - Add `@Override` annotation
   - Return appropriate CollectionCategory toString()

4. **getObjSelector()**: Return object selector string  
   - Add `@Override` annotation
   - Return appropriate CollectionCategory toString()

5. **getObjSelector(Object obj)**: Return object selector for specific object
   - Add `@Override` and `protected` modifiers
   - Call and return getObjSelector()

6. **delete(FederationActionRequest request, List<Map<String, String>> objParamMapList)**: Main delete method
   - Add `@Override` annotation
   - Add debug logging for method entry
   - Find objects using findObjects method
   - Check for empty results with logging
   - Call helper method for actual deletion processing

#### Code Patterns to Follow

**Class Declaration with Fields:**
```java
public class BAC[ObjectName]DeleteProcessor extends BACDeleteProcessor {

    private static final Logger LOGGER = LogR.getLoggerInternal(BAC[ObjectName]DeleteProcessor.class.getName());

    private final Map<ObjectIdentifier, List<ConflictType>> oidToConflictMap = new HashMap<>();

    private final Map<ConflictType, String> conflictTypeToMessage = new HashMap<>();
```

**getConflictElements Pattern:**
```java
@Override
public List<ConflictElement> getConflictElements(FederationActionRequest request,
        List<Map<String, String>> objParamMap) throws WTException {

    List<ConflictElement> conflictElementList = new ArrayList<>(super.getConflictElements(request, objParamMap));
    this. oidToConflictMap.clear();
    this.conflictTypeToMessage.clear();

    WTSet objects = new WTHashSet(findObjects(request, objParamMap).values());
    WTSet conflictingObjects = new WTHashSet();

    // TODO: Add object iteration and conflict checking
    // Iterator<[ObjectType]> itr = objects.persistableIterator([ObjectType]. class, true);
    // while (itr.hasNext()) {
    //     checkConflict(itr.next(), conflictingObjects);
    // }

    // TODO: Add conflict resolution logic
    return conflictElementList;
}
```

**findByIdentityParams Pattern:**
```java
@Override
protected Map<Object, WTReference> findByIdentityParams(List<Map<String, String>> objParamMapList)
        throws WTException {
    if (LOGGER.isDebugEnabled()) {
        LOGGER.debug("findByIdentityParams() started.  objParamMapList - " + objParamMapList);
    }
    Map<Object, WTReference> result = new HashMap<>();

    // TODO:  Implement identity-based object finding logic
    return result;
}
```

**Object Type Methods Pattern:**
```java
@Override
public String getObjType() {
    return CollectionCategory.[OBJECT_NAME].toString();
}

@Override
public String getObjSelector() {
    return CollectionCategory.[OBJECT_NAME].toString();
}

@Override
protected String getObjSelector(Object obj) {
    return getObjSelector();
}
```

**delete Method Pattern:**
```java
@Override
public void delete(FederationActionRequest request, List<Map<String, String>> objParamMapList) throws WTException {
    if (LOGGER.isDebugEnabled()) {
        LOGGER.debug("delete() started. objParamMap - " + objParamMapList);
    }

    Map<Object, WTReference> locatedObjects = findObjects(request, objParamMapList);
    if (locatedObjects == null || locatedObjects.isEmpty()) {
        if (LOGGER.isDebugEnabled())
            LOGGER.debug("No objects found for delete");
        return;
    }
    if (LOGGER.isDebugEnabled()) {
        LOGGER.debug("The following objects found for deletion - " + locatedObjects.keySet());
    }

    // TODO: Process objects for deletion
    // process[ObjectName]Deletes(new WTHashSet(locatedObjects. values()), request);
}
```

#### Private Helper Methods to Implement

1. **checkConflict([ObjectType] obj, WTSet conflictingObjects)**: Check for conflicts on object
2. **checkCheckoutConflict([ObjectType] obj, WTSet conflictingObjects)**: Check checkout conflicts
3. **processSkip(Collection<[ObjectType]> objects)**: Process skipped objects
4. **processDelete(Collection<[ObjectType]> objects, FederationActionRequest request, boolean isRefresh)**: Process deletions
5. **process[ObjectName]Deletes(WTSet objects, FederationActionRequest request)**: Main delete processing

#### Helper Method Patterns

**processSkip Pattern:**
```java
private void processSkip(Collection<[ObjectType]> objects) throws WTException {
    String deleteMsg = new WTMessage(ixbResource.class.getName(), ixbResource.BAC_SKIPPED, null)
            .getLocalizedMessage();
    for ([ObjectType] obj : objects) {
        String identity = BACIXBHelper.getIdentityFromObject(obj, getObjSelector(obj));
        BACIXBHelper.setStatusInDeleteCache(identity, deleteMsg, true);
        String summary = BACIXBHelper.DELETE_SKIPPED_DUE_TO_CONFLICT;
        BACIXBHelper.setImportSummaryInDeleteCache(identity, summary);
        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug("[ObjectName] skipped while delete - " + obj.getName());
        }
    }
}
```

**processDelete Pattern:**
```java
private void processDelete(Collection<[ObjectType]> objects, FederationActionRequest request, 
        boolean isRefreshBeforeDeln) throws WTException {
    String deleteMsg = new WTMessage(ixbResource.class. getName(), ixbResource.BAC_DELETED, null)
            .getLocalizedMessage();
    for ([ObjectType] obj :  objects) {
        String identity = BACIXBHelper.getIdentityFromObject(obj, getObjSelector(obj));
        BACIXBHelper.setStatusInDeleteCache(identity, deleteMsg, true);
        BACIXBHelper.setImportSummaryInDeleteCache(identity, BACIXBHelper.DELETE_SUCCESSFUL);
        
        // TODO: Add actual deletion logic
        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug("[ObjectName] deleted.  Identity - " + identity);
        }
    }
}
```

#### Conflict Handling Patterns

**Conflict Checking Pattern:**
```java
private void checkConflict([ObjectType] obj, WTSet conflictingObjects) throws WTException {
    checkCheckoutConflict(obj, conflictingObjects);
    // TODO: Add other conflict checks (control branch, etc.)
}
```

**Checkout Conflict Pattern:**
```java
private void checkCheckoutConflict([ObjectType] obj, WTSet conflictingObjects) throws WTException {
    if (WorkInProgressHelper.isCheckedOut(obj)) {
        String identity = BACIXBHelper. getIdentityFromObject(obj, getObjSelector(obj));
        // TODO: Add conflict handling logic for checked out objects
        conflictingObjects.add(obj);
    }
}
```

#### Critical Rules

1. **DO NOT implement interface** - Always extend `BACDeleteProcessor`
2. **Use static Logger** - Initialize with class name
3. **Initialize conflict maps** - Use HashMap for tracking
4. **Clear maps in getConflictElements** - Reset state for each conflict check
5. **Use proper logging levels** - Debug for method entry/exit, info for important operations
6. **Handle exceptions properly** - Wrap exceptions in WTException as needed
7. **Add @Override annotations** - For all overridden methods
8. **Use BACIXBHelper** - For cache operations and identity management

- DO NOT add any more method than specified above without TODO comments
- If there is any method that is not specified above, add it as a comment with TODO for business logic
- Do not implement complex business logic that is not specified above
- Do not read any other file after user provide a specific file name to read
- Do not create any super class method if it is not specified above
- Create private helper methods as needed with TODO comments for business logic

#### Exception Handling

- **WTException**:  Primary exception type for most operations
- **WTPropertyVetoException**: Handle in delete operations, wrap in WTException
- **QueryException, PersistenceException**:  Handle in query operations
- **VersionControlException**: Handle in version control operations

#### Dependencies and Imports

```java
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import org.apache.logging.log4j.Logger;
import com.ptc.windchill.  bac.BACHelper;
import com.ptc. windchill. bac.CollectionCategory;
import com.  ptc.windchill. bac.delegate.BACDeleteProcessor;
import com.ptc.windchill.bac.delete.conflict.DeleteConflictResolver;
import com.ptc. windchill.  bac.delete.conflict.resolution.DeleteResolution;
import com.ptc.windchill. bac.delete.conflict.type.DeleteConflictType;
import wt.clients.ixb. ixbResource;
import wt.conflict.ConflictElement;
import wt.conflict. ConflictServerHelper;
import wt.conflict.ConflictType;
import wt.conflict.ResolutionType;
import wt.fc.ObjectIdentifier;
import wt. fc.WTReference;
import wt.fc.  collections.WTHashSet;
import wt.fc.collections.WTSet;
import wt.fedInfra.  FederationActionRequest;
import wt. ixb.bac.BACIXBHelper;
import wt.  log4j. LogR;
import wt.util.WTException;
import wt.util.WTMessage;
import wt. vc.wip.WorkInProgressHelper;
```

### Import Guidelines
- Include comprehensive imports for conflict handling
- Include BACIXBHelper for cache operations
- Include logging and exception handling imports
- Include federation and collection imports
- Include version control helper imports for checkout checking
- Ensure no unused imports are present

### Business Logic Guidelines
- **Minimal implementation**:  Focus on structure and conflict patterns
- **Use TODO comments** for complex business logic
- **Ask user for conflict types** to include in processor
- **Keep processors generic** for easy extension
- **Follow existing patterns** from analyzed delete processor files
- **Use helper methods** for complex operations
- **Implement proper logging** at appropriate levels

### Conflict Resolution Guidelines

1. **Conflict Types**:  Define object-specific conflict types (checkout, version control, etc.)
2. **Resolution Types**: Use standard resolutions (SKIP, RETRY, UNDO_CHECKOUT_DELETE)
3. **Conflict Elements**: Create conflict elements with appropriate resolutions
4. **Conflict Tracking**: Use maps to track conflicts by object and type
5. **Cache Operations**: Use BACIXBHelper for status and conflict caching

### Method Signature Guidelines
- `getConflictElements`: `public List<ConflictElement> getConflictElements(FederationActionRequest request, List<Map<String, String>> objParamMap) throws WTException`
- `findByIdentityParams`: `protected Map<Object, WTReference> findByIdentityParams(List<Map<String, String>> objParamMapList) throws WTException`
- `delete`: `public void delete(FederationActionRequest request, List<Map<String, String>> objParamMapList) throws WTException`
- `getObjType`: `public String getObjType()`
- `getObjSelector`: `public String getObjSelector()`

### Validation Checklist
Before finalizing the generated delete processor: 
- [ ] Extends BACDeleteProcessor (not implements interface)
- [ ] Contains proper package declaration for object package
- [ ] Includes all necessary imports for conflict handling and federation
- [ ] Uses static Logger with proper class name
- [ ] Declares conflict tracking maps as private final fields
- [ ] Implements getConflictElements with @Override annotation
- [ ] Clears conflict maps at start of getConflictElements
- [ ] Implements findByIdentityParams with proper signature
- [ ] Implements delete method with proper logging and error handling
- [ ] Implements object type and selector methods
- [ ] Uses BACIXBHelper for cache operations
- [ ] Includes private helper methods with TODO comments
- [ ] Handles exceptions properly throughout
- [ ] No unused imports or unnecessary code
- [ ] TODO comments mark complex business logic
