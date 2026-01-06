# BatchPreviewDelegate Creation Guide

### Overview
This guide provides comprehensive instructions for creating BAC batch preview delegate classes that implement BACBatchPreviewDelegate in the Windchill BAC (Business Administration Console) module.

### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing batch preview delegate patterns and implementations**
- **ANALYZE batch preview delegate structure and methodology**
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
- `object_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/client/delegates/preview/`
- `preview_delegate_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/client/delegates/preview/impl/`
- `directory` = `com/ptc/windchill/bac/client/delegates/preview/impl/`
- `service_path` = `com/ptc/windchill/bac/client/BAC-delegates.xconf`
- `object.json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {object_path}

# Show directory structure
ls -la

# Find batch preview delegate files specifically
find .  -name "*BatchPreviewDelegate*. java" -type f

# Show file count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr
```

### Batch Preview Delegate File Discovery and Analysis Process
```bash
# Read Batch Preview Delegate Java files
find .  -name "*BatchPreviewDelegate*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**: List all batch preview delegate files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**:  Read that file completely and provide detailed analysis
4. **Fourth**:  Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which batch preview delegate should be created
6. **Sixth**:  Identify base interface methods that need to be implemented
7. **Finally**: Generate a new batch preview delegate class following identified patterns

### Object Dependencies Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available attributes and dependencies of that object from `object.json`
3. **Third**: Ask user to select which attributes to include in the preview delegate

### Batch Preview Delegate Class Generation Steps
1. **First**: Create a new Java class file named `Batch[ObjectName]PreviewDelegate.java`
2. **Second**:  Implement `BACBatchPreviewDelegate` interface
3. **Third**: Implement core methods:  `getDetailsOfObjects()`, `getDetailsOfDeletedObjects()`
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Add proper logging using static Log4j2 Logger
6. **Sixth**: Create instance initialization block for locale and labels
7. **Seventh**: Create static helper methods for query criteria
8. **Eighth**: **Generate minimal business logic - focus on structure and method signatures**
9. **Finally**: Save the generated file in `output_folder`

### Batch Preview Delegate Guidelines (Based on BatchDocumentTemplatePreviewDelegate Pattern)

#### Class Structure
- **Package**: `com.ptc.windchill. bac.client.delegates.preview.impl`
- **Implements**: `BACBatchPreviewDelegate`
- **Logger**: Use static Log4j2 Logger: `LogR.getLoggerInternal(ClassName.class.getName())`
- **Instance Fields**: Use final fields for locale and labels initialized in instance block

#### Class Declaration Pattern
```java
public class Batch[ObjectName]PreviewDelegate implements BACBatchPreviewDelegate {

    private static final Logger logger = LogR. getLoggerInternal(Batch[ObjectName]PreviewDelegate.class.getName());

    private final Locale LOCALE;
    private final String IDENTITY_LABEL;
    private final String VERSION_LABEL;

    {
        try {
            LOCALE = SessionHelper.getLocale();
            IDENTITY_LABEL = WTMessage.getLocalizedMessage(BACResource.class. getName(), BACResource.IDENTITY, null, LOCALE);
            VERSION_LABEL = WTMessage.getLocalizedMessage(BACClientResource.class.getName(), BACClientResource.VERSION,
                null, LOCALE);
        } catch (WTException wte) {
            throw new ExceptionInInitializerError(wte);
        }
    }
```

#### Core Methods to Implement

1. **getDetailsOfObjects(WTCollection persistables)**: Get details of regular objects
   - Add `@Override` and `@SuppressWarnings("unchecked")` annotations
   - Create HashMap for results
   - Filter collection using subCollection() for specific object type
   - Return empty map if collection is empty
   - Build QuerySpec using BatchPreviewDelegateHelper
   - Append select attributes for object details
   - Execute query and process results
   - Build PersistableDeltaInfo objects using helper methods
   - Return map of WTReference to PersistableDeltaInfo

2. **getDetailsOfDeletedObjects(WTCollection persistables)**: Get details of deleted objects
   - Add `@Override` and `@SuppressWarnings("unchecked")` annotations
   - Filter collection for BACGenericDeleteRecord objects
   - Filter by collection category using removeIf()
   - Return empty map if collection is empty
   - Build delete record QuerySpec using BatchPreviewDelegateHelper
   - Append collection category criteria
   - Execute query and process results
   - Build PersistableDeltaInfo objects for delete records
   - Return map of WTReference to PersistableDeltaInfo

#### Static Helper Methods

1. **appendUserModifiedByCriteria(QuerySpec s)**: Add user modification criteria
   - Use public static modifier
   - Add proper JavaDoc documentation
   - Get class indices using BatchPreviewDelegateHelper
   - Append select attribute for user name
   - Add search condition for user modification

#### Code Patterns to Follow

**getDetailsOfObjects Pattern:**
```java
@SuppressWarnings("unchecked")
@Override
public Map<WTReference, PersistableDeltaInfo> getDetailsOfObjects(WTCollection persistables) throws WTException {
    Map<WTReference, PersistableDeltaInfo> details = new HashMap<>();
    WTCollection templates = persistables.subCollection([ObjectType]. class, true);
    if (templates.isEmpty()) {
        return details;
    }
    
    QuerySpec spec = BatchPreviewDelegateHelper.initializeQuerySpecWithCommonAttributes([ObjectType].class);
    // TODO: Add object-specific select attributes
    spec.appendSelectAttribute([ObjectType].NAME, 0, false);
    // spec.appendSelectAttribute("iterationInfo. identifier. iterationId", 0, false);
    // spec.appendSelectAttribute("versionInfo.identifier.versionId", 0, false);
    
    BatchPreviewDelegateHelper. appendContextCriteria(spec, [ObjectType].class);
    appendUserModifiedByCriteria(spec);
    spec.appendAnd();
    spec.appendWhere(new SearchCondition([ObjectType].class, WTAttributeNameIfc.ID_NAME, templates.toIdArray()),
            new int[] { 0 });

    QueryResult result = PersistenceHelper.manager.find(spec);

    for (Object[] row : (ArrayList<Object[]>) Collections.list(result)) {
        PersistableDeltaInfo info = BatchPreviewDelegateHelper.buildCommonAttributeValues(row)
                .name(String.class. cast(row[3]))
                // TODO: Add object-specific details
                // . details(VERSION_LABEL, String.class. cast(row[5]) + "." + String.class.cast(row[4]))
                // .description(String.class.cast(row[6]))
                .context(String.class.cast(row[7]))
                .modifiedBy(String.class.cast(row[8])).toInfo();
        details.put(ObjectReference.newObjectReference(info. oid), info);
    }
    return details;
}
```

**getDetailsOfDeletedObjects Pattern:**
```java
@SuppressWarnings("unchecked")
@Override
public Map<WTReference, PersistableDeltaInfo> getDetailsOfDeletedObjects(WTCollection persistables)
        throws WTException {
    WTCollection objects = persistables.subCollection(BACGenericDeleteRecord.class);
    objects.removeIf(p -> ((BACDeleteRecord) (((ObjectReference) p).getObject()))
            .getCollectionCategory() != CollectionCategory.[OBJECT_NAME]);

    if (objects.isEmpty()) {
        return new HashMap<>();
    }

    QuerySpec spec = BatchPreviewDelegateHelper.initializeDeleteRecordQuerySpec(BACGenericDeleteRecord.class, objects);
    spec.appendAnd();
    BACGenericDeleteRecordHelper.appendCollectionCategoryCriteria(spec, CollectionCategory.[OBJECT_NAME]);
    final int deleteRecordIdx = spec.getFromClause().getPosition(BACGenericDeleteRecord.class);
    spec.appendSelectAttribute(BACGenericDeleteRecord.NAME, deleteRecordIdx, false);
    spec.appendSelectAttribute(BACGenericDeleteRecord.BAC_DELETE_INFO + "." + BACDeleteInfo.OBJECT_IDENTITY,
        deleteRecordIdx, false);
    spec.appendAnd();
    BatchPreviewDelegateHelper.appendContextCriteriaForDeleteRecord(spec, BACGenericDeleteRecord.class);
    BatchPreviewDelegateHelper.appendContainerOwnerModifiedByCriteria(spec);

    QueryResult rowResult = PersistenceHelper. manager.find(spec);

    Map<WTReference, PersistableDeltaInfo> objectToDeltaInfoMap = new HashMap<>();
    for (Object[] row : (ArrayList<Object[]>) Collections.list(rowResult)) {
        PersistableDeltaInfo info =
            BatchPreviewDelegateHelper. buildCommonAttributeValues(row)
                .name((String) row[3])
                .details(IDENTITY_LABEL, BatchPreviewDelegateHelper.readDeleteRecordIdentity(row[4]))
                .context((String) row[5])
                .modifiedBy((String) row[6]).toInfo();

        objectToDeltaInfoMap.put(ObjectReference.newObjectReference(info.oid), info);
    }
    return objectToDeltaInfoMap;
}
```

**Static Helper Method Pattern:**
```java
/**
 * Add a criteria to return the user name of the user that's related to the [ObjectName]s that's related to the
 * joinClass.
 *
 * NOTE: This api assumes that appendContextCriteria has already been called!!! 
 */
public static void appendUserModifiedByCriteria(QuerySpec s) throws WTException {
    final int objectIdx = BatchPreviewDelegateHelper.getClassIdx(s, [ObjectType].class);
    final int userIdx = BatchPreviewDelegateHelper.getClassIdx(s, WTUser.class);

    s.appendSelectAttribute(WTUser.NAME, userIdx, false);
    s.appendAnd();
    s.appendWhere(
            new SearchCondition(
                    new ClassAttribute([ObjectType].class, "iterationInfo.modifier.key. id"),
                    SearchCondition.EQUAL,
                    new ClassAttribute(WTUser.class, WTAttributeNameIfc.ID_NAME)),
            new int[] { objectIdx, userIdx });
}
```

#### Query Building Patterns

**Initialize QuerySpec with Common Attributes:**
```java
QuerySpec spec = BatchPreviewDelegateHelper.initializeQuerySpecWithCommonAttributes([ObjectType].class);
```

**Append Object-Specific Attributes:**
```java
spec.appendSelectAttribute([ObjectType].NAME, 0, false);
// spec.appendSelectAttribute("iterationInfo. identifier.iterationId", 0, false);
// spec.appendSelectAttribute("versionInfo.identifier. versionId", 0, false);
// spec.appendSelectAttribute([ObjectType].ITERATION_NOTE, 0, false);
```

**Append Context and User Criteria:**
```java
BatchPreviewDelegateHelper.appendContextCriteria(spec, [ObjectType].class);
appendUserModifiedByCriteria(spec);
```

**Filter by Object Collection:**
```java
spec.appendAnd();
spec.appendWhere(new SearchCondition([ObjectType].class, WTAttributeNameIfc.ID_NAME, templates.toIdArray()),
        new int[] { 0 });
```

#### PersistableDeltaInfo Building Patterns

**For Regular Objects:**
```java
PersistableDeltaInfo info = BatchPreviewDelegateHelper.buildCommonAttributeValues(row)
        .name(String.class.cast(row[3]))
        .details(VERSION_LABEL, String.class.cast(row[5]) + "." + String.class.cast(row[4]))
        .description(String.class.cast(row[6]))
        .context(String.class.cast(row[7]))
        .modifiedBy(String.class.cast(row[8])).toInfo();
```

**For Delete Records:**
```java
PersistableDeltaInfo info = BatchPreviewDelegateHelper.buildCommonAttributeValues(row)
        .name((String) row[3])
        .details(IDENTITY_LABEL, BatchPreviewDelegateHelper.readDeleteRecordIdentity(row[4]))
        .context((String) row[5])
        .modifiedBy((String) row[6]).toInfo();
```

#### Collection Filtering Patterns

**Filter by Object Type:**
```java
WTCollection templates = persistables.subCollection([ObjectType].class, true);
```

**Filter Delete Records by Collection Category:**
```java
WTCollection objects = persistables.subCollection(BACGenericDeleteRecord.class);
objects.removeIf(p -> ((BACDeleteRecord) (((ObjectReference) p).getObject()))
        .getCollectionCategory() != CollectionCategory.[OBJECT_NAME]);
```

#### Critical Rules

1. **DO NOT extend class** - Always implement `BACBatchPreviewDelegate` interface
2. **Use instance initialization block** - For locale and label initialization
3. **Use BatchPreviewDelegateHelper** - For all query building operations
4. **Handle empty collections** - Return empty map if collection is empty
5. **Use @SuppressWarnings("unchecked")** - For collections processing
6. **Filter collections properly** - Use subCollection() and removeIf() patterns
7. **Build PersistableDeltaInfo correctly** - Use helper methods and proper casting

- DO NOT add any more method than specified above
- If there is any method that is not specified above, add it as a comment with TODO for business logic
- Do not implement any business logic that is not specified above
- Do not read any other file after user provide a specific file name to read
- Do not create any super class method if it is not specified above
- Create static helper methods as needed following the pattern

#### Exception Handling

- **WTException**:  Primary exception type for most operations
- **ExceptionInInitializerError**: Use in instance initialization block for WTException
- Handle query exceptions appropriately
- Let most exceptions propagate to caller

#### Dependencies and Imports

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util. Locale;
import java.util. Map;
import org.apache.logging.log4j.Logger;
import com.ptc.windchill.bac.BACDeleteInfo;
import com.ptc. windchill.bac.BACDeleteRecord;
import com.ptc.windchill.bac. BACGenericDeleteRecord;
import com.ptc.windchill.bac.BACGenericDeleteRecordHelper;
import com.ptc.windchill.bac.BACResource;
import com.ptc. windchill.bac.CollectionCategory;
import com.ptc.windchill.bac.client.delegates.preview.BACBatchPreviewDelegate;
import com.ptc.windchill.bac.client.delegates.preview.impl.BatchPreviewDelegateHelper;
import com.ptc.windchill.bac.client.model.PersistableDeltaInfo;
import com.ptc.windchill.bac.client. resources.BACClientResource;
import wt.fc.ObjectReference;
import wt.fc.PersistenceHelper;
import wt.fc.QueryResult;
import wt.fc.WTReference;
import wt.fc.collections.WTCollection;
import wt. log4j.LogR;
import wt.org.WTUser;
import wt.query.ClassAttribute;
import wt.query.QuerySpec;
import wt.query.SearchCondition;
import wt.session.SessionHelper;
import wt.util.WTAttributeNameIfc;
import wt.util.WTException;
import wt.util.WTMessage;
```

### Import Guidelines
- Include comprehensive imports for query building and result processing
- Include BatchPreviewDelegateHelper and related helper classes
- Include PersistableDeltaInfo and related client model classes
- Include resource bundle imports for localized messages
- Include exception handling imports
- Ensure no unused imports are present

### Business Logic Guidelines
- **Minimal implementation**: Focus on structure and query patterns
- **Use TODO comments** for complex attribute selection
- **Ask user for object attributes** to include in preview
- **Keep delegates generic** for easy extension
- **Follow existing patterns** from analyzed batch preview delegate files
- **Use helper classes** for all query building operations

### Attribute Selection Guidelines

1. **Common Attributes**: Always included via BatchPreviewDelegateHelper
2. **Object-Specific Attributes**: Name, version info, iteration info, description
3. **Context Information**: Container/context path information
4. **User Information**: Modified by user information
5. **Custom Attributes**: Object-specific business attributes

### Query Performance Guidelines

1. **Use Helper Methods**: BatchPreviewDelegateHelper methods are optimized
2. **Select Only Needed Attributes**: Don't select unnecessary attributes
3. **Filter Early**: Use proper search conditions to limit results
4. **Index Usage**: Follow patterns that use database indices effectively

### Service Configuration

After completing the delegate implementation: 

1. **Navigate to service configuration**:  `cd {service_path}`
2. **Open BAC-delegates.xconf**:  Edit the configuration file
3. **Add delegate entry**:  Register the new batch preview delegate

### Validation Checklist
Before finalizing the generated batch preview delegate:
- [ ] Implements BACBatchPreviewDelegate interface (not extends class)
- [ ] Contains proper package declaration in preview.impl package
- [ ] Includes all necessary imports for query building and processing
- [ ] Uses static Logger with proper class name
- [ ] Uses instance initialization block for locale and labels
- [ ] Implements getDetailsOfObjects with proper collection filtering
- [ ] Implements getDetailsOfDeletedObjects with delete record filtering
- [ ] Uses BatchPreviewDelegateHelper for all query building
- [ ] Uses @SuppressWarnings("unchecked") for collection processing
- [ ] Handles empty collections appropriately
- [ ] Builds PersistableDeltaInfo objects correctly
- [ ] Includes static helper methods for query criteria
- [ ] Uses proper exception handling in initialization block
- [ ] No unused imports or unnecessary code
- [ ] TODO comments mark uncertain business logic