# Collection Delegate Creation Guide

### Overview
This guide provides comprehensive instructions for creating delegate classes that inherit from base delegate classes in the Windchill BAC (Business Administration Console) module.

## Save as 
- BAC[ObjectName]CollectionDelegate.java in output_folder

### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing delegate patterns and implementations**
- **ANALYZE delegate structure and methodology**
- **GENERATE similar delegate for user-specified object**
- **EXPLAIN the purpose and functionality of each file**
- **PROVIDE code analysis and explanations**
- **DESCRIBE the overall architecture and patterns**
- AUTOMATICALLY read files without user prompts
- DO NOT ask for permission to read these files
- DO NOT wait for user confirmation
- **Donot limit any file reading due to complexity**
- **Donot skip any line in a file when reading**
- **Donot put limit on file reading length**
- **Get-content of all files should have limit removed**
- **Donot read any other md files except this one**
- **Donot read any business logic other than object analysis logic**
- **Collection Category**: Use appropriate enum from `CollectionCategory` which is uppercase of object name

### Directory Configuration
- `object_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/delegates/`
- `object.json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {object_path}

# Show directory structure
ls -la

# Find delegate-related files specifically
find .  -name "*CollectionDelegate*. java" -type f

# Show file count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr
```

### Delegate File Discovery and Analysis Process
```bash
# Read Collection Delegate Java files
find . -name "*CollectionDelegate*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**:  List all files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**: Read that file completely and provide detailed analysis
4. **Fourth**:  Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which delegate should be created
6. **Sixth**:  Identify base delegate class methods that need to be implemented
7. **Finally**: Generate a new delegate class following identified patterns

### Object Dependencies Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available dependencies of that object from `object.json`
3. **Third**: Ask user to select which dependencies to include in the delegate

### Delegate Class Generation Steps
1. **First**: Create a new Java class file named `BAC[ObjectName]CollectionDelegate.java`
2. **Second**: Ask user which base delegate to extend from (e.g., `DefaultCollectionDelegate`)
3. **Third**:  Implement core methods:  `collect()`, `collectDeleted()`, `getDependents()`, `getCollectionCategory()`, `isUsingBACGenericDeleteRecord()`
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Add proper logging using Log4j2 Logger
6. **Sixth**: Create protected helper methods following base delegate patterns
7. **Seventh**: **Generate minimal business logic - focus on structure and method signatures**
8. **Finally**: Save the generated file in `output_folder`

### Delegate Guidelines (Based on DefaultCollectionDelegate Pattern)

#### Class Structure
- **Package**: `[object_package]. bac`
- **Extends**: `DefaultCollectionDelegate` 
- **Logger**: Use Log4j2 Logger:  `LogR.getLoggerInternal(YourClassName.class.getName())`
- **Protected Fields**:
  - `CollectionCategory collectionCategory` - stores the collection category (inherited)
  - `Class<? > objClass` - stores the persistable object class (inherited from base class)


#### Note
- Do not create method `initialize()`, it is inherited from base class
- As mention in QuerySpec below, Use same pattern in collectDeleted method for delete record class
- Add everything in try-catch block for WTException where class loading is involved
- Use `executeORefSpec(collnQuery)` for query execution, not `PersistenceHelper.manager.find()`

#### Core Methods to Implement

- Use WTHashSet for returning collections

1. **collect(BACCollectionSpec spec)**: Main collection method
   - Add `@Override` annotation
   - Add `final` modifier to method signature
   - Call `initialize(spec)` first
   - Create `QuerySpec` using `getOrefQueryForPersistable(objClass)`
   - Use `SearchCondition` for query criteria
   - Call `appendDateRangeCriteria` for date filtering using pattern: 
     ```java
     if (spec.getDateRange() != null) {
             if (collnQuery.getConditionCount() != 0) {
                collnQuery.appendAnd();
            }
         BACCollectionSvrHelper.appendDateRangeCriteria(collnQuery, objClass, spec. getDateRange());
     }
     ```
   - Execute query using `executeORefSpec(collnQuery)`
   - Return WTHashSet of deflated objects

2. **collectDeleted(BACRawCollectionSpec spec)**: Collect deleted records
   - **Only implement if `isUsingBACGenericDeleteRecord()` returns `false`**
   - Declare `Class<?> deleteRecordClass` outside try-catch
   - Get delete record class from ObjRegistryHelper
   - Use `ObjRegistryHelper.getDeleteRecordClass(spec.getCollectionCategory())` to get delete record class
   - try-catch for ClassNotFoundException
   - Create QuerySpec for delete record class
   - Apply date range criteria if provided
   - Execute and return results

3. **getDependents(WTCollection collection)**: Collect dependent objects
   - Add `@Override` annotation
   - Return empty WTHashSet if collection is null or empty
   - Add debug logging for empty collection
   - Use `collection.subCollection(ObjectClass.class).persistableIterator()` pattern
   - Get ObjectReference of dependents within iterator loop
   - Add trace logging for dependency references
   - Check if ObjectReference key is not null before adding
   - Return combined WTHashSet of all dependents

4. **getCollectionCategory()**: Return collection category
   - Add `@Override` and `protected` modifiers
   - Return appropriate `CollectionCategory` enum value
   - Example: `return CollectionCategory.DOCUMENTTEMPLATE;`

5. **isUsingBACGenericDeleteRecord()**:  Indicate delete record usage
   - Add `@Override` and `protected` modifiers
   - Return `true` if using generic delete records, `false` for custom implementation
   - If returns `true`, `collectDeleted()` method is not needed

#### Protected Helper Methods
- `executeORefSpec(collnQuery)` - Execute query and return WTHashSet
- `getOrefQueryForPersistable(objClass)` - Create base QuerySpec for object class

#### Code Patterns to Follow

**QuerySpec Creation with SearchCondition:**
```java
QuerySpec collnQuery = getOrefQueryForPersistable(objClass);
collnQuery.appendWhere(new SearchCondition(objClass, AttributeName.ATTRIBUTE, SearchCondition.CONDITION_TYPE),
        new int[] { 0 });
```

**Multiple Conditions:**
```java
collnQuery.appendAnd();
collnQuery.appendWhere(new SearchCondition(objClass, AttributeName.ATTRIBUTE, SearchCondition.CONDITION_TYPE, value),
        new int[] { 0 });
```

**Date Range Filtering:**
```java
if (spec.getDateRange() != null) {
    if (collnQuery.getConditionCount() != 0) {
                collnQuery.appendAnd();
            }
    BACCollectionSvrHelper.appendDateRangeCriteria(collnQuery, objClass, spec.getDateRange());
}
```

**Collection Iteration with SubCollection:**
```java
Iterator iterator = collection.subCollection(ObjectClass.class).persistableIterator();
while (iterator.hasNext()) {
    ObjectClass obj = (ObjectClass) iterator.next();
    ObjectReference objRef = obj.getDependentReference();
    if (objRef.getKey() != null) {
        dependentCollection.add(objRef);
    }
}
```

**Collection Category:**
```java
CollectionCategory TEMPLATE_UPPERCASE = toCollectionCategory("Template");
return CollectionCategory.TEMPLATE_UPPERCASE;
```

#### Critical Rules

1. **DO NOT create Constructor** - Use protected fields initialization in `initialize()` method
2. **DO NOT create getter/setter methods** for dependencies
3. **Use executeORefSpec()** for query execution, not PersistenceHelper.manager.find()
4. **Return WTHashSet or WTCollection** for collections
5. **Add proper null checks** before processing collections
6. **Use debug/trace logging** following the pattern in example delegates
7. **Handle ClassNotFoundException** when loading classes
8. **Use ObjectReference** for dependency objects within iterator loops
9. **Add @Override annotations** for all overridden methods
10. **Use SearchCondition** for query criteria instead of direct SQL
11. **Check ObjectReference. getKey() != null** before adding to collections
12. **Use subCollection() pattern** for type-specific collection iteration

- DO NOT add any more method than specified above
- If there is any method that is not specified above, add it as a comment with TODO for business logic
- Do not implement any business logic that is not specified above
- Do not read any other file after user provide a specific file name to read 
- Do not create any super class method if it is not specified above
- Do not create any additional helper methods unless specified above 

#### Logging Guidelines
- Debug level:  Method entry/exit, collection sizes, empty collection checks
- Trace level: Detailed object content, dependency references (use sparingly)
- Info level: Missing configurations, important state changes
- Error level:  Exceptions and error conditions

#### Dependencies and Imports
```java
import java.util.Iterator;
import org.apache.logging.log4j.Logger;
import com.ptc.windchill. bac.BACCollectionSpec;
import com.ptc. windchill.bac.BACCollectionSvrHelper;
import com.ptc.windchill.bac.CollectionCategory;
import com.ptc.windchill.bac.delegates.DefaultCollectionDelegate;
import com.ptc.windchill.bac.ObjRegistryHelper;
import wt.fc.ObjectReference;
import wt.fc.collections.WTCollection;
import wt.fc.collections.WTHashSet;
import wt.log4j.LogR;
import wt.query.QuerySpec;
import wt.query.SearchCondition;
import wt.util.WTException;
```

### Import Guidelines
- Use proper import statements for all classes used in the delegate
- Include SearchCondition for query building
- Include Iterator for collection iteration
- Ensure no unused imports are present
- Follow Windchill coding standards for import organization

### Business Logic Guidelines
- **Minimal implementation**: Focus on structure and query patterns
- **Use TODO comments** for complex business logic
- **Reference base delegate methods** for standard operations
- **Ask user for clarification** on domain-specific logic
- **Keep delegates generic** for easy extension
- **Suggest business logic approach** in TODO comments without implementing
- **Use SearchCondition patterns** from existing delegates
- **Follow subCollection iteration patterns** for type safety

### SearchCondition Types Reference
Common SearchCondition types used in delegates:
- `SearchCondition.IS_TRUE` - For boolean true conditions
- `SearchCondition.IS_FALSE` - For boolean false conditions  
- `SearchCondition.NOT_EQUAL` - For inequality conditions
- `SearchCondition.EQUAL` - For equality conditions
- `SearchCondition.IS_NULL` - For null checks
- `SearchCondition.IS_NOT_NULL` - For non-null checks

### Method Signature Templates

```java
@Override
public final WTCollection collect(BACCollectionSpec spec) throws WTException

@Override  
public WTCollection getDependents(WTCollection collection) throws WTException

@Override
protected CollectionCategory getCollectionCategory()

@Override
protected boolean isUsingBACGenericDeleteRecord()
```

### Validation Checklist
Before finalizing the generated delegate: 
- [ ] Extends correct base delegate class (DefaultCollectionDelegate)
- [ ] Implements all required interface methods with @Override annotations
- [ ] Contains proper package declaration
- [ ] Includes all necessary imports including SearchCondition
- [ ] Has Logger instance correctly configured
- [ ] Protected fields are properly declared (inherited)
- [ ] Query patterns use SearchCondition and executeORefSpec()
- [ ] Date range filtering is correctly implemented
- [ ] Null checks are in place for collections and ObjectReference keys
- [ ] Debug/trace logging is added at key points
- [ ] Uses subCollection() pattern for type-specific iteration
- [ ] getCollectionCategory() returns appropriate enum value
- [ ] isUsingBACGenericDeleteRecord() returns correct boolean
- [ ] TODO comments mark uncertain business logic

