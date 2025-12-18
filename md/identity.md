# Identity Delegate Creation Guide

### Overview
This guide provides comprehensive instructions for creating BAC identity delegate classes that extend from BACIdentityDelegateImpl in the Windchill BAC (Business Administration Console) module.

### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing identity delegate patterns and implementations**
- **ANALYZE identity delegate structure and methodology**
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
- `object_path` = `//wsl. localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/delegates/`
- `identity_delegate_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/wt/[object_package]/bac/`
- `object. json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {object_path}

# Show directory structure
ls -la

# Find identity delegate files specifically
find . -name "*IdentityDelegate*.java" -type f

# Show file count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr
```

### Identity Delegate File Discovery and Analysis Process
```bash
# Read Identity Delegate Java files
find . -name "*IdentityDelegate*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**:  List all identity delegate files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**: Read that file completely and provide detailed analysis
4. **Fourth**:  Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which identity delegate should be created
6. **Sixth**:  Identify required identity attributes and patterns
7. **Finally**: Generate a new identity delegate class following identified patterns

### Object Attributes Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available attributes of that object from `object.json`
3. **Third**: Ask user to select which attributes to include in the identity construction
4. **Fourth**: Ask user about the identity format pattern to use

### Identity Delegate Class Generation Steps
1. **First**: Create a new Java class file named `BAC[ObjectName]IdentityDelegate.java`
2. **Second**:  Extend from `BACIdentityDelegateImpl`
3. **Third**: Implement core methods:  `getIdentityFromElement()`, `getIdentityFromObject()`, `getIdentityMessageFromObject()`
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Add proper logging using static Log4j2 Logger
6. **Sixth**: Create static helper methods for identity construction
7. **Seventh**: **Generate minimal business logic - focus on structure and method signatures**
8. **Finally**: Save the generated file in `output_folder`

### Identity Delegate Guidelines (Based on BACDocTemplateIdentityDelegate Pattern)

#### Class Structure
- **Package**: `wt.[object_package]. bac`
- **Extends**: `BACIdentityDelegateImpl`
- **Logger**: Use static Log4j2 Logger:  `LogR.getLoggerInternal(ClassName.class.getName())`
- **Static Helper Methods**: Include static methods for identity construction

#### Core Methods to Implement

1. **getIdentityFromElement(IxbElement element)**: Extract identity from XML element
   - Add `@Override` annotation
   - Check for null element with info logging
   - Extract attribute values using `element.getValue()`
   - Construct identity using helper method
   - Put secured identity in cache using `BACIXBHelper.putSecuredIdentityInCache()`
   - Add debug logging for result
   - Return identity string

2. **getIdentityFromObject(Object obj)**: Extract identity from object instance
   - Add `@Override` annotation
   - Check `instanceof` for specific object type
   - Get identity message and localize it
   - Handle access control with `AccessControlHelper.manager.hasAccess()`
   - Use secured information for non-accessible objects
   - Put secured identity in cache
   - Add debug logging
   - Return identity string

3. **getIdentityMessageFromObject(Object obj)**: Get identity as WTMessage
   - Add `@Override` annotation
   - Use `SessionServerHelper.manager.setAccessEnforced(false)` pattern
   - Call static helper method in try-finally block
   - Restore original access enforcement setting
   - Return WTMessage object

#### Static Helper Methods

1. **getIdentity([ObjectType] obj)**: Static helper for object identity
   - Extract required attributes from object
   - Use helper classes for attribute extraction
   - Call private getIdentity method with parameters
   - Return WTMessage object

2. **getIdentity(String attr1, String attr2, String attr3)**: Private static helper
   - Create WTMessage with BACResource
   - Use formatted string pattern for identity
   - Return WTMessage object

#### Code Patterns to Follow

**Class Declaration:**
```java
public class BAC[ObjectName]IdentityDelegate extends BACIdentityDelegateImpl {
    private static final Logger LOGGER = LogR.getLoggerInternal(BAC[ObjectName]IdentityDelegate.class. getName());
```

**getIdentityFromElement Pattern:**
```java
@Override
public String getIdentityFromElement(IxbElement element) throws WTException {
    String name;
    String identity;
    if (element == null) {
        if (LOGGER.isInfoEnabled()) {
            LOGGER. info("No element found for [ObjectName] information.");
        }
        name = null;
        identity = null;
    } else {
        name = element.getValue(IxbHndHelper.XML_ATTR_NAME);
        // TODO: Extract other required attributes
        // String containerPath = element.getValue(IxbHndHelper.XML_ATTR_OBJECT_CONTAINER_PATH);
        // String versionId = element.getValue(IxbHndHelper.XML_ATTR_VERSION_ID) + "."
        //         + element.getValue(IxbHndHelper.XML_ATTR_ITERATION_ID);
        
        WTMessage idMsg = getIdentity(name, containerPath, versionId);
        identity = idMsg.getLocalizedMessage(SessionHelper.manager.getServerLocale());
        BACIXBHelper.putSecuredIdentityInCache(identity, identity);
    }
    if (LOGGER.isDebugEnabled()) {
        LOGGER.debug("Getting Identity from element finished.  name-" + name + " -> identity - " + identity);
    }
    return identity;
}
```

**getIdentityFromObject Pattern:**
```java
@Override
public String getIdentityFromObject(Object obj) throws WTException {
    String identity = null;
    if (obj instanceof [ObjectType]) {
        identity = getIdentityMessageFromObject(obj).getLocalizedMessage(SessionHelper. manager.getServerLocale());
        String securedInfo = identity;
        if (! AccessControlHelper.manager.hasAccess(obj, AccessPermission.READ)) {
            if (LOGGER.isInfoEnabled()) {
                LOGGER.info("No access on [ObjectName].  Returning secured info for object identity.");
            }
            ResourceBundle rb = ResourceBundle.getBundle(wt.access.accessResource.class.getName(),
                    SessionHelper.manager. getServerLocale());
            securedInfo = rb.getString(accessResource.SECURED_INFORMATION);
        }

        BACIXBHelper. putSecuredIdentityInCache(identity, securedInfo);

        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug("Identity of [ObjectName] " + (([ObjectType]) obj).getName() + " is " + identity);
        }
    }
    return identity;
}
```

**getIdentityMessageFromObject Pattern:**
```java
@Override
public WTMessage getIdentityMessageFromObject(Object obj) throws WTException {
    boolean originalPermission = SessionServerHelper.manager.setAccessEnforced(false);
    try {
        return getIdentity(([ObjectType]) obj);
    } finally {
        SessionServerHelper. manager.setAccessEnforced(originalPermission);
    }
}
```

**Static Helper Methods Pattern:**
```java
public static WTMessage getIdentity([ObjectType] obj) throws WTException {
    return getIdentity(obj.getName(), 
            IxbHndHelper.getPathOfContainer(obj. getContainerReference()),
            VersionControlHelper.getIterationDisplayIdentifier(obj).getLocalizedMessage(SessionHelper.getLocale()));
}

private static WTMessage getIdentity(String name, String containerPath, String versionId) {
    return new WTMessage(BACResource.class.getName(), BACResource.OBJ_IDENTITY,
            new Object[] { String.format("%1$s, %2$s (%3$s)", name, versionId, containerPath) });
}
```

#### Attribute Extraction Patterns

**From XML Element:**
- `element.getValue(IxbHndHelper.XML_ATTR_NAME)` - Object name
- `element.getValue(IxbHndHelper.XML_ATTR_OBJECT_CONTAINER_PATH)` - Container path
- `element.getValue(IxbHndHelper.XML_ATTR_VERSION_ID)` - Version ID
- `element.getValue(IxbHndHelper.XML_ATTR_ITERATION_ID)` - Iteration ID

**From Object Instance:**
- `obj.getName()` - Object name
- `IxbHndHelper.getPathOfContainer(obj.getContainerReference())` - Container path
- `VersionControlHelper.getIterationDisplayIdentifier(obj).getLocalizedMessage(SessionHelper.getLocale())` - Version string

#### Identity Format Patterns

Common identity format patterns:
- **Name and Version**: `"%1$s (%2$s)", name, version`
- **Name, Version, Container**:  `"%1$s, %2$s (%3$s)", name, version, containerPath`
- **Full Identity**: `"%1$s - %2$s [%3$s]", name, type, container`

#### Access Control Handling

**Access Check Pattern:**
```java
if (!AccessControlHelper.manager.hasAccess(obj, AccessPermission.READ)) {
    if (LOGGER.isInfoEnabled()) {
        LOGGER.info("No access on [ObjectName]. Returning secured info for object identity.");
    }
    ResourceBundle rb = ResourceBundle.getBundle(wt. access.accessResource.class.getName(),
            SessionHelper.manager. getServerLocale());
    securedInfo = rb.getString(accessResource.SECURED_INFORMATION);
}
```

**Session Management Pattern:**
```java
boolean originalPermission = SessionServerHelper. manager.setAccessEnforced(false);
try {
    // Identity extraction logic
    return result;
} finally {
    SessionServerHelper.manager.setAccessEnforced(originalPermission);
}
```

#### Cache Operations

Always use `BACIXBHelper.putSecuredIdentityInCache()` to cache identity information:
```java
BACIXBHelper.putSecuredIdentityInCache(identity, securedInfo);
```

#### Critical Rules

1. **DO NOT implement interface** - Always extend `BACIdentityDelegateImpl`
2. **Use static Logger** - Initialize with class name
3. **Check for null elements** - Add null checks with appropriate logging
4. **Handle access control** - Check permissions and use secured information
5. **Use helper classes** - For attribute extraction (IxbHndHelper, VersionControlHelper)
6. **Cache identities** - Always use BACIXBHelper for caching
7. **Add proper logging** - Debug for results, info for access issues
8. **Use session management** - Disable access enforcement when needed

- DO NOT add any more method than specified above
- If there is any method that is not specified above, add it as a comment with TODO for business logic
- Do not implement any business logic that is not specified above
- Do not read any other file after user provide a specific file name to read
- Do not create any super class method if it is not specified above
- Create static helper methods as needed following the pattern

#### Exception Handling

- **WTException**: Primary exception type for most operations
- Handle null checks gracefully with appropriate logging
- Let exceptions propagate to caller in most cases

#### Dependencies and Imports

```java
import java.util.ResourceBundle;
import org.apache.logging.log4j.Logger;
import com.ptc.windchill. bac.BACResource;
import com.ptc.windchill.bac.delegates.BACIdentityDelegateImpl;
import wt.access.AccessControlHelper;
import wt.access.AccessPermission;
import wt. access.accessResource;
import wt.facade. ixb.IxbElement;
import wt. ixb.bac.BACIXBHelper;
import wt.ixb.publicforhandlers.IxbHndHelper;
import wt.log4j.LogR;
import wt.session.SessionHelper;
import wt.session.SessionServerHelper;
import wt.util.WTException;
import wt. util.WTMessage;
import wt. vc.VersionControlHelper;
```

### Import Guidelines
- Include access control imports for permission checking
- Include session management imports for access enforcement control
- Include helper class imports for attribute extraction
- Include logging and resource bundle imports
- Include BACIXBHelper for cache operations
- Ensure no unused imports are present

### Business Logic Guidelines
- **Minimal implementation**: Focus on structure and identity construction patterns
- **Use TODO comments** for complex identity format logic
- **Ask user for identity format** before generating format strings
- **Keep delegates generic** for easy extension
- **Follow existing patterns** from analyzed identity delegate files
- **Use helper classes** for complex attribute extraction

### Identity Construction Guidelines

1. **Attribute Selection**: Choose attributes that uniquely identify the object
2. **Format Consistency**: Use consistent formatting across similar objects
3. **Localization**: Always use localized messages with proper locale
4. **Access Security**: Handle secured information for non-accessible objects
5. **Cache Management**: Always cache both identity and secured information

### Logging Guidelines
- Debug level:  Method results, identity values, attribute extraction
- Info level: Access control issues, null element warnings
- Use consistent logging patterns across all methods
- Include object names in debug messages when available

### Method Signature Guidelines
- `getIdentityFromElement`: `public String getIdentityFromElement(IxbElement element) throws WTException`
- `getIdentityFromObject`: `public String getIdentityFromObject(Object obj) throws WTException`
- `getIdentityMessageFromObject`: `public WTMessage getIdentityMessageFromObject(Object obj) throws WTException`
- Static helpers: `public static WTMessage getIdentity([ObjectType] obj) throws WTException`

### Validation Checklist
Before finalizing the generated identity delegate: 
- [ ] Extends BACIdentityDelegateImpl (not implements interface)
- [ ] Contains proper package declaration for object package
- [ ] Includes all necessary imports for access control and helpers
- [ ] Uses static Logger with proper class name
- [ ] Implements getIdentityFromElement with null checks and logging
- [ ] Implements getIdentityFromObject with instanceof check and access control
- [ ] Implements getIdentityMessageFromObject with session management
- [ ] Includes static helper methods for identity construction
- [ ] Uses BACIXBHelper for caching operations
- [ ] Handles access control with secured information fallback
- [ ] Uses appropriate helper classes for attribute extraction
- [ ] Includes proper logging at debug and info levels
- [ ] TODO comments mark uncertain business logic