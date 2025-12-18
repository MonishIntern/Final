# BAC Report Delegate Test Generation Instructions

## Overview

This instruction file guides the generation of unit test classes for BAC (Business Analytics Collection) report delegates. The tests focus on validating report generation for Windchill objects, ensuring proper handling of new/update/delete collections, locale support, and identity extraction for reporting purposes.

**Target Pattern**: `BAC{ObjectType}ReportDelegateTest. java`
**Example**:  `BACWTChangeOrder2ReportDelegateTest.java`

## Directory Configuration

- **Package Structure**: `wt. {domain}.bac`
- **Test Location**: Same package as the report delegate class
- **Naming Convention**: `{ReportDelegateClassName}Test.java`
- `object.json` = `c:/FINAL/.github/object.json`

## Read Information from object.json
- **Object Type**: Extract the Windchill object type for spec processing`
- **Collect all field of Object**: Extract all fields related to the object type for test generation

## Delegate Access

BAC report delegates typically implement these core interfaces: 
- Report generation via `getRows(WTSet newObjects, WTSet updateObjects, WTSet deleteObjects, Locale locale)`
- Identity extraction via `getIdentityForAccessibleObject(Persistable object, Locale locale)`
- Object formatting and localization for reporting
- Collection processing for different operation types (new, update, delete)
- Report table row creation and population

## Analysis Workflow

1. **Identify Object Type**: Determine the Windchill object type for report generation
2. **Validate Collection Handling**:  Ensure proper processing of new/update/delete collections
3. **Test Locale Support**: Verify localization functionality for different locales
4. **Test Identity Extraction**: Validate identity string creation for report display
5. **Test Edge Cases**: Handle null parameters, empty collections, and large datasets
6. **Verify Inheritance**: Confirm proper inheritance from DefaultReportDelegate

## Object Dependencies and Attributes Extraction

### Core Report Components: 
- New objects collection (WTHashSet of primary objects)
- Update objects collection (WTHashSet of modified objects)
- Delete objects collection (WTHashSet of delete records)
- Locale for internationalization
- BACReportTableRow for result formatting

### Report Generation Patterns:
- Collection processing and validation
- Object identity extraction and formatting
- Locale-specific string generation
- Report table row creation and population
- Mixed collection type handling

## Delegate Test Class Generation Steps

### 1. Class Structure Setup
```java
public class BAC{ObjectType}ReportDelegateTest {
    private BAC{ObjectType}ReportDelegate reportDelegate;
    private WTHashSet newObjects;
    private WTHashSet updateObjects;
    private WTHashSet deleteObjects;
    private Locale locale;
}
```

### 2. Test Setup Method
```java
@Before
public void setUp() {
    reportDelegate = new BAC{ObjectType}ReportDelegate();
    newObjects = new WTHashSet();
    updateObjects = new WTHashSet();
    deleteObjects = new WTHashSet();
    locale = Locale.US;
}
```

### 3. Core Test Methods
Generate tests for each core method following the patterns below. 

## Delegates Guidelines

### Core Methods to Test

#### Constructor Tests
- **testConstructor**: Verify proper initialization of report delegate instance

#### getRows() Method Tests
- **testGetRowsWithAllNullCollections**: Test all null collection parameters
- **testGetRowsWithEmptyCollections**: Test empty collection handling
- **testGetRowsWithNewObjectsOnly**: Test new objects collection processing
- **testGetRowsWithUpdateObjectsOnly**: Test update objects collection processing
- **testGetRowsWithDeleteObjectsOnly**: Test delete objects collection processing
- **testGetRowsWithAllCollectionsPopulated**: Test processing all collection types together
- **testGetRowsWithNullLocale**: Test null locale handling
- **testGetRowsWithDifferentLocales**: Test multiple locale support
- **testGetRowsWithLargeCollections**: Test performance with large datasets
- **testGetRowsMultipleInvocations**: Test consistency across multiple calls

#### getIdentityForAccessibleObject() Method Tests
- **testGetIdentityForAccessibleObjectWithNull**: Test null object handling
- **testGetIdentityForAccessibleObjectWithValidObject**: Test valid object identity extraction
- **testGetIdentityForAccessibleObjectWithNameOnly**: Test object with name attribute only
- **testGetIdentityForAccessibleObjectWithNumberOnly**: Test object with number attribute only
- **testGetIdentityForAccessibleObjectWithDifferentType**: Test non-target object type
- **testGetIdentityForAccessibleObjectWithNullLocale**:  Test null locale handling
- **testGetIdentityForAccessibleObjectWithSpecialCharacters**: Test special character handling

#### Inheritance Tests
- **testInheritance**: Verify proper inheritance from DefaultReportDelegate

### Protected Helper Methods

When present in the report delegate, test helper methods that: 
- Process specific collection types
- Format object data for reporting
- Create and populate report table rows
- Handle locale-specific formatting
- Extract and format identity information

### Code Pattern to Follow

#### Standard Test Method Pattern: 
```java
/**
 * Test [method description and expected behavior]
 */
@Test
public void test[MethodName][Scenario]() throws WTException {
    // Arrange
    [Setup test data - objects, collections, locale]
    
    // Act
    [Execute method under test]
    
    // Assert
    Assert.assertNotNull("Result should not be null", result);
    [Additional assertions for expected behavior]
}
```

#### Object Creation Pattern:
```java
{ObjectType}Master {objectMaster} = new {ObjectType}Master();
{ObjectType} {objectInstance} = new {ObjectType}();
{objectInstance}.setMaster({objectMaster});
{objectInstance}.setName("Test{ObjectType}");
{collectionName}. add({objectInstance});
```

#### Delete Record Creation Pattern:
```java
BAC{ObjectType}DeleteRecord deleteRecord = new BAC{ObjectType}DeleteRecord();
deleteRecord.setName("Deleted{ObjectType}");
deleteObjects.add(deleteRecord);
```

#### Report Generation Test Pattern:
```java
List<BACReportTableRow> result = reportDelegate.getRows(newObjects, updateObjects, deleteObjects, locale);
Assert.assertNotNull("Result should not be null", result);
```

#### Identity Extraction Test Pattern:
```java
String result = reportDelegate.getIdentityForAccessibleObject({objectInstance}, locale);
Assert.assertNotNull("Result should not be null", result);
Assert.assertTrue("Result should contain expected content", result.contains("expectedValue"));
```

## Critical Rules

### 1. Collection Handling
- All methods must handle null collections gracefully
- Return non-null List<BACReportTableRow> for getRows() (empty list if no data)
- Handle empty collections without errors
- Support processing multiple collection types simultaneously

### 2. Locale Support
- Handle null locale appropriately (use default or graceful fallback)
- Support multiple locales for internationalization testing
- Maintain consistent behavior across different locales
- Validate locale-specific formatting where applicable

### 3. Identity Extraction
- Return empty string for null objects in getIdentityForAccessibleObject()
- Extract meaningful identity information (name, number, etc.)
- Handle objects with missing or null identity attributes
- Support non-target object types through parent delegation

### 4. Exception Handling
- Handle `WTPropertyVetoException` when setting object properties in tests
- Ensure `WTException` is properly declared in method signatures
- Document expected vs. actual behavior for edge cases
- Handle object creation and setup exceptions gracefully

## Logging Guidelines

### Test Documentation
- Include comprehensive JavaDoc comments for test classes
- Document the purpose of report generation and expected output format
- Explain expected behavior for each collection type and scenario
- Note any object-specific reporting requirements or formatting

### Assertion Messages
- Provide clear assertion messages that explain expected behavior
- Use consistent message format:  "Expected behavior description"
- Example: `Assert.assertNotNull("Result should not be null", result);`
- Include context about which collections or attributes are being validated

### Helper Class Documentation
- Document any helper classes used for testing (e.g., TestPersistable)
- Explain the purpose of mock implementations
- Include TODO comments for auto-generated method stubs
- Maintain consistent formatting for helper class implementations

## Dependencies and Import

### Required Test Framework Imports
```java
import org.junit.Assert;
import org. junit.Before;
import org.junit.Test;
```

### Java Standard Library Imports
```java
import java.sql.SQLException;
import java.util.List;
import java.util.Locale;
```

### BAC Framework Imports
```java
import com.ptc.windchill. bac.BACReportTableRow;
```

### Windchill Core Imports
```java
import wt.fc.InvalidAttributeException;
import wt.fc.PersistInfo;
import wt.fc.Persistable;
import wt.fc.collections.WTHashSet;
import wt.introspection.ClassInfo;
import wt.introspection.WTIntrospectionException;
import wt. pds.PersistentRetrieveIfc;
import wt.pds.PersistentStoreIfc;
import wt.pom.DatastoreException;
import wt.util.WTException;
import wt.util.WTPropertyVetoException;
```

### Object-Specific Imports
Import the specific Windchill object type, master, and delete record: 
```java
import wt.{domain}.{ObjectType};
import wt.{domain}. {ObjectType}Master;
```

## Import Statements

### Standard Import Order: 
1. Java standard library imports (java.sql. *, java.util.*)
2. JUnit framework imports
3. BAC framework imports
4. Windchill object-specific imports
5. Windchill core framework imports
6. Report delegate class import (the class being tested)

### Example Import Block:
```java
import java.sql.SQLException;
import java.util.List;
import java.util.Locale;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import com.ptc.windchill. bac.BACReportTableRow;

import wt.change2.WTChangeOrder2;
import wt.change2.WTChangeOrder2Master;
import wt.fc.InvalidAttributeException;
import wt.fc.PersistInfo;
import wt.fc.Persistable;
import wt.fc.collections.WTHashSet;
import wt. introspection.ClassInfo;
import wt.introspection. WTIntrospectionException;
import wt.pds. PersistentRetrieveIfc;
import wt. pds.PersistentStoreIfc;
import wt.pom.DatastoreException;
import wt.util. WTException;
import wt.util.WTPropertyVetoException;
```

## Validation Checklist

### Before Test Generation: 
- [ ] Identify object type and its corresponding delete record class
- [ ] Verify report delegate class exists and proper inheritance
- [ ] Confirm object type, master class, and delete record availability
- [ ] Check for any custom reporting logic or formatting requirements

### After Test Generation:
- [ ] Constructor test validates proper initialization
- [ ] All core methods have comprehensive test coverage
- [ ] Collection handling tests cover null, empty, and populated scenarios
- [ ] Locale support tested with multiple locales and null handling
- [ ] Identity extraction tests cover various object states and types
- [ ] Return type validation confirms List<BACReportTableRow> and String types
- [ ] Inheritance test confirms proper class hierarchy

### Code Quality Checks:
- [ ] All imports are present and correctly ordered
- [ ] JavaDoc comments are comprehensive and accurate
- [ ] setUp() method properly initializes all test fixtures
- [ ] WTPropertyVetoException is properly handled in object setup
- [ ] Test independence is maintained (fresh collections for each test)
- [ ] Consistent assertion message format used
- [ ] Proper exception declarations in method signatures
- [ ] Helper classes properly implemented with required method stubs

### Collection Processing Testing Coverage:
- [ ] Null collections handled gracefully in getRows()
- [ ] Empty collections processed without errors
- [ ] Single collection type processing (new only, update only, delete only)
- [ ] Multiple collection types processed simultaneously
- [ ] Large collection performance tested
- [ ] Mixed object types in collections handled appropriately

### Object Setup Validation:
- [ ] Primary objects properly initialized with master objects
- [ ] Object attributes set correctly (name, number, etc.)
- [ ] Delete records properly created and configured
- [ ] Collection addition/removal works correctly
- [ ] Object state validation before report processing

### Locale and Internationalization Testing Coverage:
- [ ] Null locale handling returns appropriate results
- [ ] Multiple locale support tested (US, JAPAN, etc.)
- [ ] Locale-specific formatting validated where applicable
- [ ] Consistent behavior across different locales
- [ ] Default locale fallback behavior tested

### Identity Extraction Testing Coverage:
- [ ] Null object handling returns empty string
- [ ] Valid objects return non-null identity strings
- [ ] Name-only and number-only scenarios tested
- [ ] Special characters preserved in identity strings
- [ ] Non-target object types handled with appropriate fallback
- [ ] Locale parameter respected in identity generation

### Performance and Edge Cases:
- [ ] Large collection handling tested (100+ objects)
- [ ] Multiple invocation consistency verified
- [ ] Memory usage considerations for large datasets
- [ ] Special character handling in object attributes
- [ ] Thread safety considerations for report generation
- [ ] Helper class implementations include proper method stubs

### Helper Class Implementation:
- [ ] TestPersistable class properly implements Persistable interface
- [ ] All required interface methods implemented with stubs
- [ ] Serial version UID included for serializable classes
- [ ] TODO comments included for auto-generated method stubs
- [ ] toString() method provides meaningful representation