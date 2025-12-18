# BAC Collection Delegate Test Generation Instructions

## Overview

This instruction file guides the generation of unit test classes for BAC (Business Analytics Collection) collection delegates. The tests focus on validating collection methods for Windchill objects, ensuring proper handling of active and deleted objects, and testing dependency resolution.

**Target Pattern**: `BAC{ObjectType}CollectionDelegateTest. java`
**Example**:  `BACWTChangeOrder2CollectionDelegateTest.java`

## Directory Configuration

- **Package Structure**: `wt.{domain}.bac`
- **Test Location**: Same package as the delegate class
- **Naming Convention**: `{DelegateClassName}Test.java`
- `object.json` = `c:/FINAL/.github/object.json`

## Read Information from object.json
- **Object Type**: Extract the Windchill object type for spec processing`
- **Collect all field of Object**: Extract all fields related to the object type for test generation

## Delegate Access

BAC collection delegates typically implement these core interfaces: 
- Collection of active objects via `collect(BACCollectionSpec)`
- Collection of deleted objects via `collectDeleted(BACRawCollectionSpec)`
- Dependency resolution via `getDependents(WTSet)`


## Analysis Workflow

1. **Identify Object Type**: Determine the Windchill object type being collected
2. **Validate Collection Categories**: Ensure proper `CollectionCategory` enum usage
3. **Test Exception Handling**: Verify null parameter handling
4. **Verify Return Types**:  Confirm `WTSet` and `WTHashSet` return types
5. **Test Multiple Invocations**: Ensure consistent behavior across calls

## Object Dependencies and Attributes Extraction

### Core Object Attributes to Consider:
- Primary keys and identifiers
- State information (active/deleted)
- Timestamps and version data
- Related object references

### Dependency Patterns:
- Parent-child relationships
- Cross-references to other Windchill objects
- Collection dependencies

## Delegate Test Class Generation Steps

### 1. Class Structure Setup
```java
public class BAC{ObjectType}CollectionDelegateTest {
    private BAC{ObjectType}CollectionDelegate collectionDelegate;
    private BACCollectionSpec collectionSpec;
    private BACRawCollectionSpec rawCollectionSpec;
}
```

### 2. Test Setup Method
```java
@Before
public void setUp() {
    collectionDelegate = new BAC{ObjectType}CollectionDelegate();
    collectionSpec = new BACCollectionSpec(CollectionCategory.{OBJECT_TYPE});
    rawCollectionSpec = new BACRawCollectionSpec(CollectionCategory.{OBJECT_TYPE});
}
```

### 3. Core Test Methods
Generate tests for each core method following the patterns below. 

## Delegates Guidelines

### Core Methods to Test

#### collect() Method Tests
- **testCollectReturnsNonNull**:  Verify non-null return value
- **testCollectWithNullSpec**: Test exception handling for null parameters
- **testCollectMultipleInvocations**: Test consistency across multiple calls
- **testCollectWithValidCategory**: Validate proper category handling

#### collectDeleted() Method Tests
- **testCollectDeletedReturnsNonNull**: Verify non-null return value
- **testCollectDeletedWithNullSpec**: Test exception handling for null parameters
- **testCollectDeletedReturnsCorrectType**: Verify `WTHashSet` return type
- **testCollectDeletedMultipleInvocations**: Test consistency across multiple calls

#### getDependents() Method Tests
- **testGetDependentsWithNull**: Handle null collection input
- **testGetDependentsWithEmptyCollection**: Handle empty collection input
- **testGetDependentsWithCollection**: Test with populated collection
- **testGetDependentsReturnsCorrectType**: Verify `WTHashSet` return type

### Protected Helper Methods

When present in the delegate, test helper methods that:
- Validate input parameters
- Transform collection specifications
- Handle specific object type logic

### Code Pattern to Follow

#### Standard Test Method Pattern: 
```java
/**
 * [Test description]
 */
@Test
public void test[MethodName][Scenario]() throws WTException {
    // Arrange
    [Setup test data]
    
    // Act
    [Execute method under test]
    
    // Assert
    Assert.assertNotNull("Result should not be null", result);
    [Additional assertions]
}
```

#### Exception Test Pattern:
```java
@Test(expected = Exception.class)
public void test[MethodName]WithNull[Parameter]() throws WTException {
    [delegate].[method](null);
}
```

## Critical Rules

### 1. Null Safety
- All public methods must handle null parameters gracefully
- Expected behavior: throw appropriate exceptions for null required parameters
- Return empty collections for null optional parameters where appropriate

### 2. Return Type Consistency
- `collect()` and `collectDeleted()` must return `WTSet` implementations
- Prefer `WTHashSet` for concrete return types
- Never return `null` - return empty collections instead

### 3. Exception Handling
- Use `@Test(expected = Exception.class)` for null parameter tests
- Catch and verify specific exception types when possible
- Ensure `WTException` is properly declared in method signatures

### 4. Test Independence
- Each test method must be independent
- Use `@Before` setUp() method for common initialization
- Avoid static state or shared test data

## Logging Guidelines

### Test Documentation
- Include comprehensive JavaDoc comments for test classes
- Document test purpose and expected behavior
- Use descriptive test method names that explain the scenario

### Assertion Messages
- Provide clear assertion messages that explain expected behavior
- Use consistent message format:  "Expected behavior description"
- Example: `Assert.assertNotNull("Result should not be null", result);`

## Dependencies and Import

### Required Test Framework Imports
```java
import org.junit.Assert;
import org. junit.Before;
import org.junit.Test;
```

### BAC Framework Imports
```java
import com.ptc.windchill.bac.BACCollectionSpec;
import com.ptc.windchill. bac.BACRawCollectionSpec;
import com.ptc.windchill.bac.CollectionCategory;
```

### Windchill Core Imports
```java
import wt.fc.collections.WTHashSet;
import wt.fc.collections.WTSet;
import wt.util.WTException;
```

### Object-Specific Imports
Import the specific Windchill object type being tested:
```java
import wt.{domain}.{ObjectType};
```

## Import Statements

### Standard Import Order: 
1. JUnit framework imports
2. BAC framework imports  
3. Windchill core framework imports
4. Domain-specific object imports
5. Delegate class import (the class being tested)

### Example Import Block:
```java
import org.junit.Assert;
import org. junit.Before;
import org. junit.Test;

import com.ptc.windchill.bac.BACCollectionSpec;
import com.ptc.windchill.bac.BACRawCollectionSpec;
import com.ptc. windchill.bac.CollectionCategory;

import wt.change2.WTChangeOrder2;
import wt.fc.collections.WTHashSet;
import wt.fc.collections.WTSet;
import wt.util.WTException;
```

## Validation Checklist

### Before Test Generation: 
- [ ] Identify correct CollectionCategory enum value
- [ ] Verify delegate class exists and is accessible
- [ ] Confirm object type import availability
- [ ] Check for any custom collection specifications

### After Test Generation:
- [ ] All core methods have corresponding tests
- [ ] Null parameter handling is tested for all public methods
- [ ] Return types are validated in tests
- [ ] Exception handling tests use appropriate expected exceptions
- [ ] Test method names are descriptive and follow naming conventions
- [ ] All imports are present and correctly ordered
- [ ] JavaDoc comments are comprehensive and accurate
- [ ] setUp() method properly initializes test fixtures
- [ ] No hardcoded values that should be parameterized
- [ ] Test independence is maintained (no static state dependencies)

### Code Quality Checks:
- [ ] No duplicate test logic
- [ ] Consistent assertion message format
- [ ] Proper exception declarations in method signatures
- [ ] Use of appropriate JUnit annotations
- [ ] Clear separation between arrange, act, and assert phases