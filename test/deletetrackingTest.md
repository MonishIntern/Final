# BAC Delete Tracking Delegate Test Generation Instructions

## Overview

This instruction file guides the generation of unit test classes for BAC (Business Analytics Collection) delete tracking delegates. The tests focus on validating delete tracking functionality, object filtering, attribute setting, and proper collection category management for deleted Windchill objects.

**Target Pattern**: `BAC{ObjectType}DeleteTrackingDelegateTest. java`
**Example**:  `BACWTChangeOrder2DeleteTrackingDelegateTest.java`

## Directory Configuration

- **Package Structure**: `wt.{domain}.bac`
- **Test Location**: Same package as the delete tracking delegate class
- **Naming Convention**: `{DeleteTrackingDelegateClassName}Test.java`
- `object.json` = `c:/FINAL/.github/object.json`

## Read Information from object.json
- **Object Type**: Extract the Windchill object type for spec processing`
- **Collect all field of Object**: Extract all fields related to the object type for test generation

## Delegate Access

BAC delete tracking delegates typically implement these core interfaces: 
- Collection category identification via `getCollectionCategory()`
- Object filtering via `filterDeletedObjs(WTSet)`
- Attribute management via `setAttributes(BACGenericDeleteRecord, Persistable)`
- Delete tracking workflow coordination
- Collection processing and validation

## Analysis Workflow

1. **Identify Object Type**: Determine the Windchill object type for delete tracking
2. **Validate Collection Category**:  Ensure proper CollectionCategory enum usage
3. **Test Object Filtering**: Verify filtering of deleted objects from collections
4. **Test Attribute Setting**: Validate attribute extraction and setting on delete records
5. **Test Collection Processing**: Handle null, empty, and populated collections
6. **Verify Inheritance**: Confirm proper inheritance from BACDefaultGenericDeleteTrackingDelegate

## Object Dependencies and Attributes Extraction

### Core Object Components: 
- Primary Windchill object (e.g., WTChangeOrder2)
- Master object (e.g., WTChangeOrder2Master)
- Collection containers (WTHashSet, WTSet)
- BACGenericDeleteRecord for tracking deleted objects

### Delete Tracking Patterns:
- Object filtering and validation
- Attribute extraction from persistable objects
- Collection category management
- Delete record creation and population

## Delegate Test Class Generation Steps

### 1. Class Structure Setup
```java
public class BAC{ObjectType}DeleteTrackingDelegateTest {
    private BAC{ObjectType}DeleteTrackingDelegate trackingDelegate;
    private WTHashSet {objectCollection};
}
```

### 2. Test Setup Method
```java
@Before
public void setUp() {
    trackingDelegate = new BAC{ObjectType}DeleteTrackingDelegate();
    {objectCollection} = new WTHashSet();
}
```

### 3. Core Test Methods
Generate tests for each core method following the patterns below. 

## Delegates Guidelines

### Core Methods to Test

#### getCollectionCategory() Method Tests
- **testGetCollectionCategory**:  Test correct collection category return
- **testGetCollectionCategoryMultipleInvocations**: Test consistency across multiple calls

#### filterDeletedObjs() Method Tests
- **testFilterDeletedObjsWithNull**: Test null collection handling
- **testFilterDeletedObjsWithEmptyCollection**: Test empty collection handling
- **testFilterDeletedObjsWithSingleObject**: Test single object processing
- **testFilterDeletedObjsWithMultipleObjects**:  Test multiple object processing
- **testFilterDeletedObjsReturnsCorrectType**:  Verify WTHashSet return type
- **testFilterDeletedObjsWithMixedTypes**: Test mixed object type handling
- **testFilterDeletedObjsWithLargeCollection**: Test performance with large collections
- **testFilterDeletedObjsMultipleInvocations**: Test consistency across multiple calls

#### setAttributes() Method Tests (Protected Method - Use Reflection)
- **testSetAttributesWithNullDeleteRecord**: Test null delete record handling
- **testSetAttributesWithNullPersistable**: Test null persistable handling
- **testSetAttributesWithValidObject**: Test valid attribute setting

#### Inheritance Tests
- **testInheritance**: Verify proper inheritance from BACDefaultGenericDeleteTrackingDelegate

### Protected Helper Methods

When present in the delete tracking delegate, test helper methods that: 
- Extract specific attributes from objects
- Validate object types before processing
- Transform object data for delete records
- Handle object-specific filtering logic

### Code Pattern to Follow

#### Standard Test Method Pattern: 
```java
/**
 * Test [method description and expected behavior]
 */
@Test
public void test[MethodName][Scenario]() throws WTException {
    // Arrange
    [Setup test data - objects, collections]
    
    // Act
    [Execute method under test]
    
    // Assert
    Assert.assertNotNull("Result should not be null", result);
    [Additional assertions for expected behavior]
}
```

#### Object Creation Pattern:
```java
{ObjectType} {objectInstance} = {ObjectType}. new{ObjectType}({ObjectType}Master.new{ObjectType}Master());
{objectInstance}.setName("Test{ObjectType}");
{objectCollection}.add({objectInstance});
```

#### Reflection Pattern for Protected Methods:
```java
try {
    java.lang.reflect.Method method = BAC{ObjectType}DeleteTrackingDelegate.class
        .getDeclaredMethod("methodName", ParameterType1.class, ParameterType2.class);
    method.setAccessible(true);
    method.invoke(trackingDelegate, parameter1, parameter2);
} catch (Exception e) {
    // Handle expected behavior
}
```

#### Collection Category Test Pattern:
```java
CollectionCategory category = trackingDelegate. getCollectionCategory();
Assert.assertNotNull("Category should not be null", category);
Assert.assertEquals("Category should be {OBJECT_TYPE}", 
                   CollectionCategory.{OBJECT_TYPE}, category);
```

## Critical Rules

### 1. Collection Handling
- All methods must handle null collections gracefully
- Return empty WTHashSet for null/empty input collections (never return null)
- Maintain collection type consistency (WTHashSet for return values)
- Handle large collections without performance degradation

### 2. Object Filtering
- Filter only the appropriate object type from mixed collections
- Preserve object references and identity during filtering
- Handle malformed or incomplete objects gracefully
- Maintain collection order when possible

### 3. Attribute Setting
- Extract attributes safely from persistable objects
- Handle null objects and null delete records gracefully
- Set attributes using proper Windchill property setting methods
- Validate attribute values before setting

### 4. Exception Handling
- Handle `WTPropertyVetoException` when setting object properties
- Use reflection properly for testing protected methods
- Ensure `WTException` is properly declared in method signatures
- Document expected vs. actual exception behavior

## Logging Guidelines

### Test Documentation
- Include comprehensive JavaDoc comments for test classes
- Document the purpose of delete tracking and object filtering
- Explain expected behavior for each test scenario
- Note any object-specific requirements or filtering logic

### Assertion Messages
- Provide clear assertion messages that explain expected behavior
- Use consistent message format:  "Expected behavior description"
- Example: `Assert.assertNotNull("Result should not be null", result);`
- Include context about which objects or attributes are being validated

### Reflection Method Testing
- Document why reflection is used for protected method testing
- Include proper error handling for reflection exceptions
- Note expected behavior when methods are called via reflection
- Handle accessibility and security considerations properly

## Dependencies and Import

### Required Test Framework Imports
```java
import org.junit.Assert;
import org. junit.Before;
import org.junit.Test;
```

### BAC Framework Imports
```java
import com.ptc.windchill. bac.BACGenericDeleteRecord;
import com. ptc.windchill.bac.CollectionCategory;
```

### Windchill Core Imports
```java
import wt.fc.Persistable;
import wt.fc.collections.WTHashSet;
import wt.fc.collections.WTSet;
import wt.util.WTException;
import wt.util.WTPropertyVetoException;
```

### Object-Specific Imports
Import the specific Windchill object type and its master: 
```java
import wt.{domain}.{ObjectType};
import wt.{domain}. {ObjectType}Master;
```

## Import Statements

### Standard Import Order: 
1. JUnit framework imports
2. BAC framework imports
3. Windchill object-specific imports
4. Windchill core framework imports
5. Delete tracking delegate class import (the class being tested)

### Example Import Block:
```java
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import com.ptc.windchill.bac.BACGenericDeleteRecord;
import com. ptc.windchill.bac.CollectionCategory;

import wt.change2.WTChangeOrder2;
import wt.change2.WTChangeOrder2Master;
import wt.fc.Persistable;
import wt.fc.collections.WTHashSet;
import wt. fc.collections.WTSet;
import wt.util.WTException;
import wt. util.WTPropertyVetoException;
```

## Validation Checklist

### Before Test Generation:
- [ ] Identify correct CollectionCategory enum value for object type
- [ ] Verify delete tracking delegate class exists and proper inheritance
- [ ] Confirm object type and master class availability
- [ ] Check for any custom filtering or attribute logic

### After Test Generation:
- [ ] Collection category tests validate correct enum values
- [ ] Object filtering tests cover null, empty, and populated collections
- [ ] Attribute setting tests use proper reflection for protected methods
- [ ] Return type validation confirms WTHashSet usage
- [ ] Inheritance test confirms proper class hierarchy
- [ ] Multiple invocation tests ensure consistency

### Code Quality Checks:
- [ ] All imports are present and correctly ordered
- [ ] JavaDoc comments are comprehensive and accurate
- [ ] setUp() method properly initializes test fixtures
- [ ] WTPropertyVetoException is properly handled in object creation
- [ ] Test independence is maintained (fresh collections for each test)
- [ ] Consistent assertion message format used
- [ ] Proper exception declarations in method signatures

### Collection Processing Testing Coverage:
- [ ] Null collection handling tested and returns empty collection
- [ ] Empty collection handling tested and returns empty collection
- [ ] Single object processing tested and preserves object
- [ ] Multiple object processing tested with correct count validation
- [ ] Mixed object types handled appropriately (filtering)
- [ ] Large collection performance tested
- [ ] Return type validation confirms WTHashSet instances

### Object Setup Validation:
- [ ] Primary objects properly initialized with master objects
- [ ] Object attributes set correctly (name, number, etc.)
- [ ] Object factory methods used when available
- [ ] Collection addition/removal works correctly
- [ ] Object state validation before processing

### Attribute Management Testing Coverage:
- [ ] Null delete record handling in setAttributes tested
- [ ] Null persistable handling in setAttributes tested
- [ ] Valid attribute setting tested with reflection
- [ ] Attribute extraction from objects validated
- [ ] Property setting exceptions handled appropriately

### Reflection Testing Validation:
- [ ] Protected method access properly implemented
- [ ] Method parameter types correctly specified
- [ ] setAccessible(true) called before method invocation
- [ ] Exception handling covers reflection-specific errors
- [ ] Method invocation results properly validated

### Performance and Scalability:
- [ ] Large collection handling tested (100+ objects)
- [ ] Multiple invocation consistency verified
- [ ] Memory usage considerations for large collections
- [ ] Collection type preservation throughout processing
- [ ] Object reference integrity maintained during filtering

### Edge Case Testing Coverage:
- [ ] Empty object names and attributes
- [ ] Objects with special characters in names
- [ ] Objects with missing required attributes
- [ ] Collection category consistency validation
- [ ] Thread safety considerations for multiple invocations