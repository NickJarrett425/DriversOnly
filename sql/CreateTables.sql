-- Team06
-- David, Dhruvisha, Neil, Nick, Ryan


CREATE SCHEMA IF NOT EXISTS onlydrivers;
USE onlydrivers;

CREATE TABLE IF NOT EXISTS `user` (
    UserID INTEGER NOT NULL,
    UserUsername VARCHAR(255) NOT NULL,
    UserEmail VARCHAR(255) NOT NULL,
    UserEncryptedPW VARCHAR(255) NOT NULL,
    UserFName VARCHAR(255) NOT NULL,
    UserLName VARCHAR(255) NOT NULL,
    UserMiddleInitial CHAR NOT NULL,
    UserType VARCHAR(15) NOT NULL,
    PRIMARY KEY (UserID)
);

CREATE TABLE IF NOT EXISTS sponsor_organization (
	SponsorOrganizationID INTEGER NOT NULL,
    SponsorOrganizationCompanyName VARCHAR(255) NOT NULL,
    SponsorOrganizationDollarValuePerPoint DOUBLE NOT NULL,
    PRIMARY KEY (SponsorOrganizationID)
);

CREATE TABLE IF NOT EXISTS driver (
	DriverID INTEGER NOT NULL,
    DriverUserID INTEGER NOT NULL,
    DriverSponsorOrganizationID INTEGER NOT NULL,
    DriverPoints INTEGER NOT NULL,
    DriverPhone VARCHAR(30) NOT NULL,
    DriverStreetLine1 VARCHAR(255) NOT NULL,
    DriverAptSuite VARCHAR(255) NOT NULL,
    DriverCity VARCHAR(255) NOT NULL,
    DriverState VARCHAR(2) NOT NULL,
    DriverZipCode VARCHAR(5) NOT NULL,
    FOREIGN KEY (DriverUserID)
		REFERENCES `user` (UserID),
	FOREIGN KEY (DriverSponsorOrganizationID)
		REFERENCES sponsor_organization (SponsorOrganizationID),		
    PRIMARY KEY (DriverID)
);

CREATE TABLE IF NOT EXISTS sponsor (
    SponsorID INTEGER NOT NULL,
    SponsorUserID INTEGER NOT NULL,
    SponsorSponsorOrganizationID INTEGER NOT NULL,
    FOREIGN KEY (SponsorUserID)
		REFERENCES `user` (UserID),
	FOREIGN KEY (SponsorSponsorOrganizationID)
		REFERENCES sponsor_organization (SponsorOrganizationID),		
    PRIMARY KEY (SponsorID)
);

CREATE TABLE IF NOT EXISTS `admin` (
    AdminID INTEGER NOT NULL,
    AdminUserID INTEGER NOT NULL,
    FOREIGN KEY (AdminUserID)
		REFERENCES `user` (UserID),
    PRIMARY KEY (AdminID)
);

CREATE TABLE IF NOT EXISTS application (
    ApplicationID INTEGER NOT NULL,
    ApplicationDriverID INTEGER NOT NULL,
    ApplicationSponsorOrganizationID INTEGER NOT NULL,
    ApplicationStatus VARCHAR(255) NOT NULL,
    ApplicationReason VARCHAR(255) NOT NULL,
    ApplicationDateSubmitted DATETIME NOT NULL,
    ApplicationDateReviewed DATETIME NOT NULL,
    FOREIGN KEY (ApplicationDriverID)
		REFERENCES driver (DriverID),
	FOREIGN KEY (ApplicationSponsorOrganizationID)
		REFERENCES sponsor_organization (SponsorOrganizationID),		
    PRIMARY KEY (ApplicationID)
);

CREATE TABLE IF NOT EXISTS vehicle (
    VehicleVIN VARCHAR(17) NOT NULL,
    VehicleDriverID INTEGER NOT NULL,
    VehicleMake VARCHAR(255) NOT NULL,
    VehicleModel VARCHAR(255) NOT NULL,
    VehicleYear YEAR(4) NOT NULL,
    VehicleInsuranceCompany VARCHAR(255) NOT NULL,
    VehiclePolicyNumber VARCHAR(255) NOT NULL,
    FOREIGN KEY (VehicleDriverID)
		REFERENCES driver (DriverID),	
    PRIMARY KEY (VehicleVIN)
);

CREATE TABLE IF NOT EXISTS catalog (
	CatalogID INTEGER NOT NULL,
    CatalogSponsorOrganizationID INTEGER NOT NULL,
    CatalogName VARCHAR(255) NOT NULL,
    FOREIGN KEY (CatalogSponsorOrganizationID)
		REFERENCES sponsor_organization (SponsorOrganizationID),		
    PRIMARY KEY (CatalogID)
);

CREATE TABLE IF NOT EXISTS `order` (
	OrderID INTEGER NOT NULL,
    OrderDriverID INTEGER NOT NULL,
    OrderTrackingNumber VARCHAR(255) NOT NULL,
    OrderTotalPointPrice INTEGER NOT NULL,
    OrderDate DATETIME NOT NULL,
    FOREIGN KEY (OrderDriverID)
		REFERENCES driver (DriverID),		
    PRIMARY KEY (OrderID)
);

CREATE TABLE IF NOT EXISTS line_item (
	LineItemID INTEGER NOT NULL,
    LineItemCatalogID INTEGER NOT NULL,
    LineItemUnitPrice INTEGER NOT NULL,
    FOREIGN KEY (LineItemCatalogID)
		REFERENCES catalog (CatalogID),	
    PRIMARY KEY (LineItemID)
);

CREATE TABLE IF NOT EXISTS order_item (
	OrderItemOrderID INTEGER NOT NULL,
    OrderItemLineID INTEGER NOT NULL,
    FOREIGN KEY (OrderItemOrderID)
		REFERENCES `order` (OrderID),
	FOREIGN KEY (OrderItemLineID)
		REFERENCES line_item (LineItemID),		
    PRIMARY KEY (OrderItemOrderID, OrderItemLineID)
);

CREATE TABLE IF NOT EXISTS catalog_line (
	CatalogLineCatalogID INTEGER NOT NULL,
    CatalogLineLineID INTEGER NOT NULL,
    FOREIGN KEY (CatalogLineCatalogID)
		REFERENCES catalog (CatalogID),
	FOREIGN KEY (CatalogLineLineID)
		REFERENCES line_item (LineItemID),	 
    PRIMARY KEY (CatalogLineCatalogID, CatalogLineLineID)
);

#CREATE TABLE IF NOT EXISTS transaction (
#	TransactionID INTEGER NOT NULL,
#    TransactionPointAmount INTEGER NOT NULL,
#   TransactionDateDATETIME NOT NULL,
#    TransactionReason VARCHAR(255) NOT NULL,
#    FOREIGN KEY ()
#		REFERENCES sponsor_org (SponsorOrgID),		
#    PRIMARY KEY (CatalogID)
#);

#CREATE TABLE IF NOT EXISTS driver_transaction (
#	DriverTransactionTransactionID INTEGER NOT NULL,
#    DriverTransactionDriverID INTEGER NOT NULL,
#    FOREIGN KEY (DriverTransactionTransactionID)
#		REFERENCES transaction (TransactionID),
#	FOREIGN KEY (DriverTransactionDriverID)
#		REFERENCES driver (DriverID),			
#    PRIMARY KEY (DriverTransactionTransactionID, DriverTransactionDriverID)
#);
