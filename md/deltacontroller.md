## Directory Configuration
- `controller_path` = `\\wsl.localhost\WindchillVM\opt\wnc\wcmod\modules\BAC\src\com\ptc\windchill\bac\client\controllers\`

## DeltaController.java Location
- Full path: `{controller_path}DeltaController.java`

## DeltaController Update Instructions

### Overview
The `DeltaController.java` file contains a `categoryFromType(Class<?> clazz)` method that maps business object classes to their corresponding `CollectionCategory` constants. When adding a new BAC object, you must:
1. Add the import statement for the persistable class
2. Register its class-to-category mapping in the method

### STEP 1: Add Import Statement

1. **Get Required Information**
   - Persistable class full qualified name (e.g., `wt.change2.WTChangeOrder2`)
   - Package path (e.g., `wt.change2`)
   - Class name (e.g., `WTChangeOrder2`)

2. **Locate Import Section**
   - Open `DeltaController.java` at the configured path
   - Find the import section at the top of the file (after package declaration)
   - Locate the group of imports that match your object's package structure
   - Domain-specific imports are typically grouped together

3. **Add Import Statement**
   Insert the import statement in alphabetical order within the appropriate group:
   ```java
   import wt.your.package.YourClassName;
   ```

4. **Import Placement Rules**
   - Core Java imports (java.*) come first
   - Third-party imports (org.*, com.*) come next
   - Windchill imports (wt.*, com.ptc.*) come last
   - Within Windchill imports, organize by package hierarchy
   - Example for `wt.change2.WTChangeOrder2`:
     ```java
     import wt.change2.WTChangeOrder2;
     import wt.change2.WTVariance;
     ```

5. **Multiple Classes from Same Package**
   If you need to import multiple classes from the same package, add them in alphabetical order:
   ```java
   import wt.change2.WTChangeOrder2;
   import wt.change2.WTVariance;
   ```

### STEP 2: Add Object Mapping in categoryFromType Method

1. **Get Required Information**
   - Template name (e.g., `WTChangeOrder2`)
   - Persistable class name (e.g., `WTChangeOrder2` - already imported)
   - CollectionCategory constant (must match template name exactly, case-sensitive)
   - Related DeleteRecord classes (if any)

2. **Locate Insertion Point**
   - Find the `categoryFromType(Class<?> clazz)` method (around line 219)
   - Identify where to add based on object type:
     - **Before the `else if(WVSConfigurationTemplate.class...` block** for most objects
     - **Before the `try` block** for special cases
   - Maintain logical grouping (similar objects together)

3. **Add Class Mapping**
   
   **For Single Class Mapping:**
   ```java
   if (YourClassName.class.isAssignableFrom(clazz)) {
       return CollectionCategory.YourTemplateName;
   }
   ```

   **For Multiple Related Classes (with DeleteRecord):**
   ```java
   if (YourClassName.class.isAssignableFrom(clazz) || YourDeleteRecordClass.class.isAssignableFrom(clazz)) {
       return CollectionCategory.YourTemplateName;
   }
   ```

4. **Formatting Rules**
   - Use 8 spaces for `if` statement indentation (2 tab levels)
   - Use 12 spaces for `return` statement indentation (3 tab levels)
   - Add blank line after the closing brace `}`
   - Maintain consistency with existing entries
   - For multiple conditions, align OR operators (`||`) on new lines with 16 spaces indentation

### Example Patterns from Existing Code

#### Import Statement Examples:
```java
// Single import
import wt.team.TeamTemplate;

// Multiple imports from same package (alphabetically ordered)
import wt.change2.WTChangeOrder2;
import wt.change2.WTVariance;

// Import with DeleteRecord class
import wt.workflow.definer.WfProcessTemplate;
import wt.workflow.definer.bac.BACWfTemplateDeleteRecord;
```

#### Mapping Examples:

**Single class mapping:**
```java
        if (LifeCycleTemplate.class.isAssignableFrom(clazz)) {
            return CollectionCategory.LIFECYCLETEMPLATE;
        }
```

**Single class mapping (actual example from code):**
```java
        if (WTChangeOrder2.class.isAssignableFrom(clazz)) {
            return CollectionCategory.WTChangeOrder2;
        }
```

**Multiple classes with OR conditions:**
```java
        if (WfProcessTemplate.class.isAssignableFrom(clazz) || BACWfTemplateDeleteRecord.class.isAssignableFrom(clazz) ||
                BACWFProxyTemplateDeleteRecord.class.isAssignableFrom(clazz) || WfProxyTemplate.class.isAssignableFrom(clazz)) {
            return CollectionCategory.WFPROCESSTEMPLATE;
        }
```

**Else-if pattern (for last entries before try block):**
```java
        } else if(WVSConfigurationTemplate.class.isAssignableFrom(clazz)) {
            return CollectionCategory.VISUALIZATION_CONFIGURATION;
        }
```

### Complete Example Workflow

**Scenario**: Adding mapping for `wt.change2.WTChangeOrder2`

**Step 1 - Add Import:**
```java
// Locate import section and add:
import wt.change2.WTChangeOrder2;
```

**Step 2 - Add Mapping:**
```java
// In categoryFromType method, add before else-if block:
        if (WTChangeOrder2.class.isAssignableFrom(clazz)) {
            return CollectionCategory.WTChangeOrder2;
        }
```

### Important Notes
- **Import First**: ALWAYS add import statement BEFORE adding the class mapping
- **Exact Names**: Use exact class names as they appear in the codebase
- **Case Sensitivity**: CollectionCategory constant is case-sensitive (usually matches template name exactly)
- **CollectionCategory**: The category constant must already be registered in `CollectionCategory.java` (Step 4 of main workflow)
- **DeleteRecord Classes**: If object has a custom DeleteRecord class, import it and include it with OR condition
- **Placement**: Add new mappings before the `else if(WVSConfigurationTemplate...` block or as appropriate
- **No Else-If for New Entries**: Use regular `if` statement for new entries in the middle; only use `else if` for the very last entry before the try block

### Validation Checklist
After making changes, verify:
1. ✓ Import statement added in correct location (alphabetically within appropriate group)
2. ✓ Proper indentation (8 spaces for `if`, 12 spaces for `return`)
3. ✓ CollectionCategory constant exists in `CollectionCategory.java`
4. ✓ Persistable class is imported at top of file
5. ✓ No duplicate mappings exist
6. ✓ Blank line added after closing brace
7. ✓ Java syntax is valid (no compilation errors)
8. ✓ Class name matches imported class exactly